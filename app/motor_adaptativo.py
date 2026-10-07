"""
Motor Adaptativo ADIF OEP 2026 (SQLite + pdftotext + Gemini 3 Flash / 2.5 Flash Lite).
Diseñado específicamente para la estructura de carpetas de /Users/carlosfernandez/Desktop/ADIF 2026/APP:
- BASES/
- TEMARIO COMÚN TÉCNICO/ (15 temas oficiales)
- TEMARIO ESPECÍFICO TÉCNICO GESTIÓN/ (6 temas oficiales)
- TEMARIO ESPECÍFICO TÉCNICO COMUNICACIÓN/ (6 temas oficiales)
- EXÁMENES AÑOS ANTERIORES/ (2021, 2022, 2023, 2024, 2025)
"""

from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import sqlite3
import subprocess
import unicodedata
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "adif_2026_estado.db"
CONFIG_PATH = BASE_DIR / "config_local.json"

# Modelos activos verificados con la clave del usuario (Gemini 3 Flash + 2.5 Flash Lite de respaldo)
MODELOS_GEMINI_ACTIVOS = [
    "gemini-3-flash-preview",
    "gemini-2.5-flash-lite",
]


def norm_nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def extraer_texto_pdf_o_txt(filepath: Path) -> str:
    """Extrae el texto completo de un PDF usando pdftotext (Poppler) o pypdf."""
    suffix = filepath.suffix.lower()
    if suffix in (".txt", ".md"):
        return filepath.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        pdftotext_bin = shutil.which("pdftotext") or "/opt/homebrew/bin/pdftotext"
        if Path(pdftotext_bin).exists():
            try:
                txt = subprocess.check_output(
                    [pdftotext_bin, str(filepath), "-"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                )
                if len(txt.strip()) > 50:
                    return txt
            except Exception:
                pass

        try:
            import pypdf  # type: ignore

            reader = pypdf.PdfReader(str(filepath))
            txt = "\n".join(page.extract_text() or "" for page in reader.pages)
            if len(txt.strip()) > 50:
                return txt
        except Exception:
            pass

    return ""


def limpiar_lineas_ruido_boe(texto: str) -> str:
    """Elimina el bloque ÍNDICE inicial del BOE, cabeceras repetitivas y líneas con puntos (. .)."""
    # Si el documento del BOE tiene la marca '[Bloque 1:' o el segundo 'TEXTO CONSOLIDADO', cortar el ÍNDICE previo
    pos_indice = texto.find("ÍNDICE")
    if pos_indice != -1 and pos_indice < 3000:
        pos_texto = texto.find("TEXTO CONSOLIDADO", pos_indice)
        if pos_texto != -1:
            texto = texto[pos_texto:]

    lineas_limpias: list[str] = []
    for linea in texto.splitlines():
        s = linea.strip()
        if ". ." in s or "....." in s:
            continue
        if s.startswith("BOLETÍN OFICIAL DEL ESTADO") or s.startswith("LEGISLACIÓN CONSOLIDADA"):
            continue
        if re.match(r"^Página\s+\d+$", s):
            continue
        lineas_limpias.append(linea)
    return "\n".join(lineas_limpias)


def _es_fragmento_valido(fragmento: str) -> bool:
    if ". ." in fragmento:
        return False
    if len(re.findall(r"(?m)^\d{1,3}\s*$", fragmento)) >= 2:
        return False
    lineas = [l.strip() for l in fragmento.splitlines() if l.strip()]
    if len(lineas) < 2:
        return False
    primera = lineas[0].lower()
    # Excluir "Artículo único. Aprobación del Estatuto/Reglamento/Texto refundido..." (decreto envoltorio con disposición derogatoria)
    if primera.startswith("artículo único") or primera.startswith("art. único"):
        return False
    # Excluir artículos de reglamentos cuya única finalidad es "Derogación"
    if len(lineas) > 1 and re.match(r"^derogaci[oó]n\.?$", lineas[1], re.IGNORECASE):
        return False
    if re.search(r"^art[ií]culo\s+\d+[\.\s]+derogaci[oó]n\b", primera, re.IGNORECASE):
        return False

    # Limpiar cabeceras estructurales (TÍTULO, CAPÍTULO, Sección) para comprobar si el artículo real está "(Derogado)" o "(Suprimido)"
    lineas_cuerpo = [
        l
        for l in lineas[1:]
        if not re.match(r"^(?:T[ÍI]TULO|CAP[ÍI]TULO|Secci[oó]n)\b", l, re.IGNORECASE)
    ]
    cuerpo = " ".join(lineas_cuerpo).strip()
    if len(cuerpo) < 65:
        return False
    if re.search(r"^\(?(?:Derogado|Suprimido|Sin contenido)\)?\.?$", cuerpo, re.IGNORECASE):
        return False
    if "(derogado)" in cuerpo.lower() and len(cuerpo) < 160:
        return False
    if "(suprimido)" in cuerpo.lower() and len(cuerpo) < 160:
        return False
    return True


def trocear_documento_adif(bloque_temario: str, documento_nombre: str, texto_bruto: str) -> list[dict[str, str]]:
    """
    Trocea cada PDF del temario de ADIF en unidades evaluables:
    - Si es una Ley/Real Decreto/Reglamento: extrae cada Artículo individualmente (saltando el índice del BOE y derogados).
    - Si es un documento técnico de ADIF (Declaración sobre la Red, Informe de Gestión, Canal Ético):
      lo divide en secciones temáticas de ~2500 caracteres para que ningún apartado quede sin evaluar.
    """
    texto = limpiar_lineas_ruido_boe(texto_bruto)
    unidades: list[dict[str, str]] = []

    patron_articulo = re.compile(
        r"(?m)^(?P<cabecera>(?:Artículo|Art\.)\s+(?:\d+|único|primero|segundo|tercero|cuarto|quinto|sexto|séptimo|octavo|noveno|décimo|undécimo|duodécimo|decimotercero|decimocuarto|decimoquinto|decimosexto|decimoséptimo|decimoctavo|decimonoveno|vigésimo)[\w\s\.ºª\-]*)"
    )
    matches = list(patron_articulo.finditer(texto))

    if len(matches) >= 3:
        vistos: set[str] = set()
        for i, m in enumerate(matches):
            inicio = m.start()
            fin = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
            fragmento = texto[inicio:fin].strip()
            # Cortar disposiciones derogatorias o finales que queden pegadas al último artículo de la ley
            fragmento = re.split(
                r"(?m)^Disposici[oó]n\s+(?:derogatoria|final|transitoria)\b",
                fragmento,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()
            if not _es_fragmento_valido(fragmento):
                continue
            cabecera_linea = fragmento.splitlines()[0].strip()
            m_cod = re.match(r"^((?:Artículo|Art\.)\s+[^\.\n]+)", cabecera_linea)
            codigo = m_cod.group(1).strip()[:40] if m_cod else cabecera_linea[:40]
            clave = codigo.lower()
            if clave in vistos and len(fragmento) < 250:
                continue
            vistos.add(clave)
            unidades.append(
                {
                    "bloque_temario": bloque_temario,
                    "documento": documento_nombre,
                    "codigo_unidad": codigo,
                    "titulo_unidad": cabecera_linea[:130],
                    "contenido_literal": fragmento[:5500],
                }
            )

    if len(unidades) < 3:
        unidades = []
        parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto) if len(p.strip()) > 60]
        buffer_actual: list[str] = []
        chars_actual = 0
        sec_idx = 1

        for p in parrafos:
            buffer_actual.append(p)
            chars_actual += len(p)
            if chars_actual >= 2200:
                bloque_txt = "\n\n".join(buffer_actual)
                primera_linea = re.sub(r"\s+", " ", buffer_actual[0])[:90]
                unidades.append(
                    {
                        "bloque_temario": bloque_temario,
                        "documento": documento_nombre,
                        "codigo_unidad": f"Apartado {sec_idx}",
                        "titulo_unidad": f"Apartado {sec_idx}: {primera_linea}",
                        "contenido_literal": bloque_txt[:5500],
                    }
                )
                sec_idx += 1
                buffer_actual = []
                chars_actual = 0

        if buffer_actual and chars_actual > 150:
            bloque_txt = "\n\n".join(buffer_actual)
            primera_linea = re.sub(r"\s+", " ", buffer_actual[0])[:90]
            unidades.append(
                {
                    "bloque_temario": bloque_temario,
                    "documento": documento_nombre,
                    "codigo_unidad": f"Apartado {sec_idx}",
                    "titulo_unidad": f"Apartado {sec_idx}: {primera_linea}",
                    "contenido_literal": bloque_txt[:5500],
                }
            )

    return unidades


def extraer_preguntas_examenes_adif(convocatoria: str, documento_nombre: str, texto: str) -> list[dict[str, str]]:
    """
    Extrae preguntas reales de Conocimiento General y Específico de los cuadernillos de ADIF
    para alimentar el ADN del Tribunal ADIF (Few-Shot).
    """
    ejemplos: list[dict[str, str]] = []
    patron_preg = re.compile(
        r"(?ms)^(?P<num>\d{1,2})\.\s+(?P<cuerpo>[^\n]+(?:\n(?!\d{1,2}\.\s)[^\n]*){2,35}?a\).+?b\).+?c\).+?d\).+?)(?=^\d{1,2}\.\s|\Z)"
    )
    for m in patron_preg.finditer(texto):
        bloque_q = m.group(0).strip()
        if len(bloque_q) < 120 or len(bloque_q) > 1800:
            continue
        if "____" in bloque_q or "What does " in bloque_q or "Choose the " in bloque_q:
            continue
        palabras_clave = (
            "ley",
            "real decreto",
            "adif",
            "artículo",
            "reglamento",
            "declaración sobre la red",
            "estatuto",
            "contrato",
            "presupuest",
            "seguridad",
            "igualdad",
            "prevención",
        )
        if not any(k in bloque_q.lower() for k in palabras_clave):
            continue

        es_incorrecta = "INCORRECTA" in bloque_q.upper() or "NO ES" in bloque_q.upper()
        patron_trampa = (
            "Pregunta de inversión negativa ('Señale la opción INCORRECTA') con 3 afirmaciones literales del BOE y 1 alterada sutilmente."
            if es_incorrecta
            else "Pregunta oficial de Tribunal ADIF: distractores largos casi idénticos donde cambia una sola cláusula ('salvo que', ámbito de aplicación RFIG, plazo o sujeto competente)."
        )
        ejemplos.append(
            {
                "documento_origen": f"{convocatoria} - {documento_nombre}",
                "enunciado": re.sub(r"\n{2,}", "\n", bloque_q),
                "patron_trampa": patron_trampa,
            }
        )
        if len(ejemplos) >= 25:
            break
    return ejemplos


def init_db() -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS unidades_temario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bloque_temario TEXT NOT NULL,
            documento TEXT NOT NULL,
            codigo_unidad TEXT NOT NULL,
            titulo_unidad TEXT NOT NULL,
            contenido_literal TEXT NOT NULL,
            nivel_actual INTEGER DEFAULT 1,
            dominio_score REAL DEFAULT 0.0,
            veces_visto INTEGER DEFAULT 0,
            aciertos_totales INTEGER DEFAULT 0,
            fallos_totales INTEGER DEFAULT 0,
            racha_aciertos INTEGER DEFAULT 0,
            prioridad_refuerzo INTEGER DEFAULT 0,
            ultimo_error_tipo TEXT DEFAULT '',
            ultimo_error_detalle TEXT DEFAULT '',
            intervalo_dias INTEGER DEFAULT 0,
            proximo_repaso TEXT DEFAULT '',
            UNIQUE(bloque_temario, documento, codigo_unidad)
        );

        CREATE TABLE IF NOT EXISTS adn_tribunal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_origen TEXT NOT NULL,
            enunciado TEXT NOT NULL,
            patron_trampa TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS banco_preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad_id INTEGER NOT NULL,
            nivel INTEGER NOT NULL,
            es_refuerzo INTEGER DEFAULT 0,
            trampa_objetivo TEXT DEFAULT '',
            enunciado TEXT NOT NULL,
            opciones_json TEXT NOT NULL,
            indice_correcta INTEGER NOT NULL,
            cita_literal_boe TEXT NOT NULL,
            explicacion_detallada TEXT NOT NULL,
            trampas_por_opcion_json TEXT NOT NULL,
            usada INTEGER DEFAULT 0,
            FOREIGN KEY(unidad_id) REFERENCES unidades_temario(id)
        );

        CREATE TABLE IF NOT EXISTS historial_respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad_id INTEGER NOT NULL,
            pregunta_id INTEGER NOT NULL,
            nivel_pregunta INTEGER NOT NULL,
            es_refuerzo INTEGER DEFAULT 0,
            opcion_elegida INTEGER NOT NULL,
            acierto INTEGER NOT NULL,
            trampa_caida TEXT DEFAULT '',
            accion_motor TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(unidad_id) REFERENCES unidades_temario(id)
        );
        """
    )
    conn.commit()
    conn.close()

    sincronizar_carpetas_adif()
    cargar_ejemplos_oficiales()
    poblar_preguntas_semilla_adif()


def sincronizar_carpetas_adif() -> dict[str, int]:
    conn = get_db_connection()
    cur = conn.cursor()
    nuevas_unidades = 0
    nuevos_patrones = 0

    for sub in sorted(BASE_DIR.iterdir()):
        if not sub.is_dir() or sub.name.startswith("."):
            continue
        nombre_norm = norm_nfc(sub.name).upper()

        if "TEMARIO" in nombre_norm:
            bloque_etiqueta = norm_nfc(sub.name)
            for pdf in sorted(sub.glob("*.pdf")):
                doc_name = norm_nfc(pdf.name)
                cur.execute(
                    "SELECT COUNT(*) FROM unidades_temario WHERE bloque_temario = ? AND documento = ?",
                    (bloque_etiqueta, doc_name),
                )
                if cur.fetchone()[0] > 0:
                    continue

                texto = extraer_texto_pdf_o_txt(pdf)
                if not texto.strip():
                    continue
                unidades = trocear_documento_adif(bloque_etiqueta, doc_name, texto)
                for u in unidades:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO unidades_temario
                        (bloque_temario, documento, codigo_unidad, titulo_unidad, contenido_literal)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            u["bloque_temario"],
                            u["documento"],
                            u["codigo_unidad"],
                            u["titulo_unidad"],
                            u["contenido_literal"],
                        ),
                    )
                    if cur.rowcount > 0:
                        nuevas_unidades += 1

        elif "EXÁMENES" in nombre_norm or "EXAMENES" in nombre_norm:
            for pdf in sorted(sub.rglob("*.pdf")):
                convocatoria = pdf.parent.name
                origen_key = norm_nfc(f"{convocatoria} - {pdf.name}")
                cur.execute("SELECT COUNT(*) FROM adn_tribunal WHERE documento_origen = ?", (origen_key,))
                if cur.fetchone()[0] > 0:
                    continue
                texto = extraer_texto_pdf_o_txt(pdf)
                if not texto.strip():
                    continue
                ejemplos = extraer_preguntas_examenes_adif(convocatoria, norm_nfc(pdf.name), texto)
                for ej in ejemplos:
                    cur.execute(
                        """
                        INSERT INTO adn_tribunal (documento_origen, enunciado, patron_trampa)
                        VALUES (?, ?, ?)
                        """,
                        (origen_key, ej["enunciado"], ej["patron_trampa"]),
                    )
                    nuevos_patrones += 1

    conn.commit()
    conn.close()
    return {"nuevas_unidades": nuevas_unidades, "nuevos_patrones_examen": nuevos_patrones}


def buscar_unidad_id(cur: sqlite3.Cursor, fragmento_doc: str, fragmento_art: str) -> int | None:
    cur.execute(
        """
        SELECT id FROM unidades_temario
        WHERE documento LIKE ? AND codigo_unidad LIKE ?
        ORDER BY id ASC LIMIT 1
        """,
        (f"%{fragmento_doc}%", f"%{fragmento_art}%"),
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "SELECT id FROM unidades_temario WHERE documento LIKE ? ORDER BY id ASC LIMIT 1",
        (f"%{fragmento_doc}%",),
    )
    row = cur.fetchone()
    return row["id"] if row else None


def poblar_preguntas_semilla_adif() -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM banco_preguntas")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    semillas = [
        {
            "doc_match": "01 RD 5_2015",
            "art_match": "Artículo 54",
            "nivel": 1,
            "es_refuerzo": 0,
            "trampa_objetivo": "Principios de conducta (Art. 54 TREBEP) - Examen Oficial ADIF",
            "enunciado": "Conforme al Real Decreto Legislativo 5/2015 (TREBEP), según el artículo 54 sobre principios de conducta, el empleado público:",
            "opciones": [
                "Podrá aceptar regalos o favores siempre que no consistan en dinero en efectivo ni superen los usos habituales.",
                "Se rechazará cualquier regalo, favor o servicio en condiciones ventajosas que vaya más allá de los usos habituales, sociales y de cortesía, sin perjuicio de lo establecido en el Código Penal.",
                "Únicamente rechazará regalos cuando provengan de contratistas directos de la entidad pública empresarial.",
                "Deberá poner en conocimiento del Ministerio Fiscal cualquier regalo que supere los 150 euros.",
            ],
            "indice_correcta": 1,
            "cita_literal_boe": "Artículo 54.3 TREBEP: «Se rechazará cualquier regalo, favor o servicio en condiciones ventajosas que vaya más allá de los usos habituales, sociales y de cortesía, sin perjuicio de lo establecido en el Código Penal.»",
            "explicacion_detallada": "Pregunta clásica del Tribunal de ADIF (aparecida en OEP 2025): el artículo 54 separa los principios éticos (art. 53) de los principios de conducta (art. 54). El rechazo de regalos más allá de los usos sociales/cortesía es un principio de conducta expreso del art. 54.3.",
            "trampas_por_opcion": [
                "Trampa de invención: el TREBEP no autoriza regalos por no ser en efectivo.",
                "Correcta: Literalidad exacta del artículo 54.3 del RDL 5/2015.",
                "Trampa restrictiva ('Únicamente'): la prohibición es general, no solo frente a contratistas.",
                "Trampa numérica: el TREBEP no fija umbral de 150 euros.",
            ],
        },
        {
            "doc_match": "04 Ley 4_2023",
            "art_match": "Artículo 44",
            "nivel": 1,
            "es_refuerzo": 0,
            "trampa_objetivo": "Procedimiento de rectificación registral (Ley 4/2023) - Examen ADIF 2025",
            "enunciado": "Según la Ley 4/2023, de 28 de febrero, para la igualdad real y efectiva de las personas trans y para la garantía de los derechos de las personas LGTBI, respecto al procedimiento de rectificación registral de la mención relativa al sexo, la persona encargada del Registro Civil deberá:",
            "opciones": [
                "Citar a la persona legitimada para que comparezca de nuevo y ratifique su solicitud en el plazo máximo de 1 mes desde la comparecencia inicial.",
                "Dictar resolución sobre la rectificación registral solicitada dentro del plazo máximo de un mes a contar desde la fecha de la primera comparecencia.",
                "Informar en la comparecencia inicial a la persona solicitante de las consecuencias jurídicas de la rectificación pretendida.",
                "Exigir informe médico o psicológico previo que acredite la disconformidad con el sexo mencionado en la inscripción de nacimiento.",
            ],
            "indice_correcta": 2,
            "cita_literal_boe": "Artículo 44.4 de la Ley 4/2023: «En la comparecencia inicial, la persona encargada del Registro Civil informará a la persona solicitante de las consecuencias jurídicas de la rectificación pretendida...»",
            "explicacion_detallada": "Pregunta literal del examen de ADIF de noviembre de 2025 (Pregunta 38). El Tribunal juega con los plazos del Art. 44: la segunda comparecencia para ratificar es en el plazo máximo de TRES meses (no 1 mes), y la resolución se dicta en el plazo máximo de UN mes desde la SEGUNDA comparecencia (no desde la primera).",
            "trampas_por_opcion": [
                "Trampa de plazo (Examen ADIF 2025): el plazo para la segunda comparecencia es de máximo 3 meses (art. 44.6), no 1 mes.",
                "Trampa de dies a quo (Examen ADIF 2025): el plazo de 1 mes para dictar resolución se cuenta desde la fecha de la SEGUNDA comparecencia (art. 44.7), no desde la primera.",
                "Correcta: Literal del artículo 44.4 de la Ley 4/2023.",
                "Prohibido expresamente por el artículo 44.3 de la Ley 4/2023.",
            ],
        },
        {
            "doc_match": "05 Ley 31_1995",
            "art_match": "Artículo 19",
            "nivel": 1,
            "es_refuerzo": 0,
            "trampa_objetivo": "Formación de los trabajadores (Art. 19 LPRL) - Examen ADIF 2025",
            "enunciado": "Según el artículo 19 de la Ley 31/1995, de Prevención de Riesgos Laborales, ¿cuándo deberá adaptarse y repetirse periódicamente la formación teórica y práctica en materia preventiva?",
            "opciones": [
                "Obligatoriamente cada seis meses para todos los puestos de trabajo.",
                "A la evolución de los riesgos y a la aparición de otros nuevos, repitiéndose periódicamente, si fuera necesario, cuando cambien las funciones o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.",
                "Únicamente cuando lo solicite por escrito el trabajador o los Delegados de Prevención.",
                "Siempre fuera de la jornada de trabajo, descontando el 50% del tiempo invertido.",
            ],
            "indice_correcta": 1,
            "cita_literal_boe": "Artículo 19.1 Ley 31/1995: «La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.»",
            "explicacion_detallada": "Pregunta real del examen ADIF 2025 (Pregunta 40).",
            "trampas_por_opcion": [
                "Trampa de plazo inventado: la ley no fija una periodicidad fija de 6 meses.",
                "Correcta: Recoge los supuestos del artículo 19.1 de la Ley 31/1995.",
                "Falso: es un deber del empresario garantizado de oficio.",
                "Trampa del art. 19.2: si se hace fuera de jornada se descuenta el 100% del tiempo invertido, no el 50%.",
            ],
        },
        {
            "doc_match": "13 Ley 9_2017",
            "art_match": "Artículo 2",
            "nivel": 1,
            "es_refuerzo": 0,
            "trampa_objetivo": "Ámbito de aplicación y concepto de contrato oneroso (Art. 2 LCSP) - Examen ADIF 2025",
            "enunciado": "¿Cuáles de los siguientes contratos quedan sometidos a la Ley 9/2017, de Contratos del Sector Público, en los términos establecidos en su artículo 2?",
            "opciones": [
                "Los contratos onerosos, cualquiera que sea su naturaleza jurídica, que celebren las entidades enumeradas en el artículo 3, entendidos como onerosos aquellos en los que el contratista obtenga algún tipo de beneficio económico, ya sea de forma directa o indirecta.",
                "Aquellos, cualquiera que sea su naturaleza jurídica, que celebren las entidades del artículo 3, salvo que el contratista obtenga algún tipo de beneficio económico directo o indirecto.",
                "Únicamente los contratos administrativos sujetos a regulación armonizada que celebren las Administraciones Públicas.",
                "Los contratos gratuitos y convenios interadministrativos, cualquiera que sea su objeto.",
            ],
            "indice_correcta": 0,
            "cita_literal_boe": "Artículo 2.1 Ley 9/2017: «Son contratos del sector público y, en consecuencia, están sometidos a la presente Ley en la forma y términos previstos en la misma, los contratos onerosos, cualquiera que sea su naturaleza jurídica, que celebren las entidades enumeradas en el artículo 3. Se entenderá que un contrato tiene carácter oneroso en los casos en que el contratista obtenga algún tipo de beneficio económico, ya sea de forma directa o indirecta.»",
            "explicacion_detallada": "Pregunta real del examen ADIF 2025 (Pregunta 39).",
            "trampas_por_opcion": [
                "Correcta: Literalidad exacta del artículo 2.1 de la LCSP 9/2017.",
                "Trampa real de ADIF 2025: invierte el sentido cambiando 'en los que' por 'salvo que'.",
                "Trampa restrictiva: la LCSP también aplica a contratos privados y no armonizados del sector público.",
                "Falso: requiere carácter oneroso.",
            ],
        },
        {
            "doc_match": "08 Declaracion sobre la red",
            "art_match": "Apartado 1",
            "nivel": 1,
            "es_refuerzo": 0,
            "trampa_objetivo": "Tráfico ferroviario transfronterizo y secciones fronterizas (Declaración sobre la Red ADIF)",
            "enunciado": "Según la Declaración sobre la Red de Adif, en las infraestructuras ferroviarias consideradas transfronterizas, reglamentariamente se podrán establecer, con objeto de facilitar el tráfico ferroviario transfronterizo, excepciones a la normativa aplicable al resto de la RFIG:",
            "opciones": [
                "No se admiten en ningún caso excepciones normativas al tráfico ferroviario dentro de la RFIG.",
                "Únicamente la referida a la exención lingüística siempre que la empresa ferroviaria lo solicite a la Dirección de Tráfico.",
                "Sobre el personal ferroviario, el material rodante, la circulación ferroviaria o los certificados de seguridad de las empresas ferroviarias, que serán de aplicación en la sección fronteriza para las circulaciones que tengan origen o destino la estación de la RFIG que delimita la sección fronteriza.",
                "Sobre el personal ferroviario, el material rodante, la circulación ferroviaria o los certificados de seguridad de las empresas ferroviarias, que serán de aplicación en toda la RFIG a la empresa ferroviaria extranjera.",
            ],
            "indice_correcta": 2,
            "cita_literal_boe": "Declaración sobre la Red de Adif (Capítulo 2 / Marco normativo transfronterizo): «Se podrán establecer excepciones reglamentariamente sobre el personal ferroviario, el material rodante, la circulación ferroviaria o los certificados de seguridad de las empresas ferroviarias, que serán de aplicación en la sección fronteriza para las circulaciones que tengan origen o destino la estación de la RFIG que delimita la sección fronteriza.»",
            "explicacion_detallada": "Pregunta real del examen ADIF 2025 (Pregunta 37).",
            "trampas_por_opcion": [
                "Falso: sí se prevén excepciones reglamentarias en secciones fronterizas.",
                "Trampa restrictiva: abarca personal, material rodante, circulación y certificados de seguridad.",
                "Correcta: Se aplica exclusivamente en la sección fronteriza hasta la estación de la RFIG que la delimita.",
                "Trampa geográfica clásica de ADIF: extiende la excepción a 'toda la RFIG' en lugar de 'la sección fronteriza'.",
            ],
        },
    ]

    for s in semillas:
        u_id = buscar_unidad_id(cur, s["doc_match"], s["art_match"])
        if not u_id:
            continue
        cur.execute(
            """
            INSERT INTO banco_preguntas (
                unidad_id, nivel, es_refuerzo, trampa_objetivo, enunciado,
                opciones_json, indice_correcta, cita_literal_boe,
                explicacion_detallada, trampas_por_opcion_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                u_id,
                s["nivel"],
                s["es_refuerzo"],
                s["trampa_objetivo"],
                s["enunciado"],
                json.dumps(s["opciones"], ensure_ascii=False),
                s["indice_correcta"],
                s["cita_literal_boe"],
                s["explicacion_detallada"],
                json.dumps(s["trampas_por_opcion"], ensure_ascii=False),
            ),
        )

    conn.commit()
    conn.close()


def obtener_api_key() -> str:
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if env_key:
        return env_key.strip()
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return data.get("gemini_api_key", "").strip()
        except Exception:
            return ""
    return ""


def guardar_api_key(api_key: str) -> None:
    CONFIG_PATH.write_text(
        json.dumps({"gemini_api_key": api_key.strip()}, indent=2),
        encoding="utf-8",
    )


def construir_filtro_sql(filtro_bloque: str, filtro_documento: str) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []

    if filtro_documento and filtro_documento not in ("TODOS", "SIMULACRO_GLOBAL", "SIMULACRO_30"):
        clauses.append("documento = ?")
        params.append(filtro_documento)
    elif filtro_bloque and filtro_bloque != "TODOS":
        if filtro_bloque == "PERFIL_GESTION":
            clauses.append("(bloque_temario LIKE '%COMÚN%' OR bloque_temario LIKE '%GESTIÓN%')")
        elif filtro_bloque == "PERFIL_COMUNICACION":
            clauses.append("(bloque_temario LIKE '%COMÚN%' OR bloque_temario LIKE '%COMUNICACIÓN%')")
        else:
            clauses.append("bloque_temario = ?")
            params.append(filtro_bloque)

    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    return where_sql, params


def seleccionar_siguiente_objetivo(filtro_bloque: str = "PERFIL_GESTION", filtro_documento: str = "TODOS") -> dict[str, Any]:
    """
    Motor determinista de selección adaptativa ADIF 2026 con rotación anti-monotonía:
    1. Artículos en Rama de Refuerzo obligatorio (fallados recientemente -> corrección inmediata).
    2. Cada 3 preguntas vistas, rescata un artículo que ya acertaste en Nivel 1 o 2 (que no sea de los últimos 3 turnos)
       para subirlo a Nivel 2 o Nivel 3.
    3. Siguiente artículo nunca visto (intercalando los distintos documentos PDF del bloque para no atascarse en una sola ley).
    4. Artículos con repaso espaciado vencido.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    ahora_iso = datetime.datetime.now().isoformat()
    where_base, params_base = construir_filtro_sql(filtro_bloque, filtro_documento)
    and_clause = where_base.replace(" WHERE ", " AND ") if where_base else ""

    # MODO EXAMEN OFICIAL: Saltarse todo el motor adaptativo (ni refuerzo, ni escalada) y coger una pregunta 100% aleatoria de todo el bloque
    if filtro_documento == "SIMULACRO_30":
        cur.execute(
            f"""
            SELECT * FROM unidades_temario
            {where_base}
            ORDER BY RANDOM()
            LIMIT 1
            """,
            params_base,
        )
        row = cur.fetchone()
        conn.close()
        return {
            "unidad": dict(row),
            "es_refuerzo": 0,
            "motivo_seleccion": "Modo Examen: Selección 100% aleatoria sin sesgos adaptativos.",
        }

    # Obtener las últimas 3 unidades preguntadas para no repetir el mismo artículo de forma consecutiva tras acertar
    cur.execute("SELECT unidad_id FROM historial_respuestas ORDER BY id DESC LIMIT 3")
    recientes_ids = [r["unidad_id"] for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM historial_respuestas")
    total_respondidas = cur.fetchone()[0] or 0

    # 1. Prioridad máxima: Rama de Refuerzo inmediata si acaba de fallar un precepto
    cur.execute(
        f"""
        SELECT * FROM unidades_temario
        WHERE prioridad_refuerzo = 1 {and_clause}
        ORDER BY fallos_totales DESC, id ASC
        LIMIT 1
        """,
        params_base,
    )
    row = cur.fetchone()
    if row:
        conn.close()
        return {
            "unidad": dict(row),
            "es_refuerzo": 1,
            "motivo_seleccion": f"Rama de Refuerzo ADIF: Fallaste recientemente este precepto ({row['ultimo_error_tipo'] or 'consolidación obligatoria'}).",
        }

    # 2. Escalada intercalada: si toca turno de escalada (cada 3 preguntas) y hay un artículo en Nivel 1/2 que NO acaba de salir
    if total_respondidas > 0 and total_respondidas % 3 == 0:
        excl_sql = ""
        excl_params: list[Any] = []
        if recientes_ids:
            placeholders = ",".join("?" for _ in recientes_ids)
            excl_sql = f" AND id NOT IN ({placeholders})"
            excl_params = recientes_ids

        cur.execute(
            f"""
            SELECT * FROM unidades_temario
            WHERE veces_visto > 0 AND dominio_score < 85 {and_clause} {excl_sql}
            ORDER BY nivel_actual ASC, veces_visto ASC
            LIMIT 1
            """,
            [*params_base, *excl_params],
        )
        row = cur.fetchone()
        if row:
            conn.close()
            return {
                "unidad": dict(row),
                "es_refuerzo": 0,
                "motivo_seleccion": f"Rama de Escalada: Subiendo a Nivel {row['nivel_actual']} este artículo tras asimilar el nivel previo.",
            }

    # 3. Cobertura de temario (Secuencial en Piloto Automático vs Aleatorio en Simulacro)
    if filtro_documento == "SIMULACRO_GLOBAL":
        # Extrae un precepto aleatorio que aún no hayamos preguntado (mezclando todas las leyes)
        cur.execute(
            f"""
            SELECT * FROM unidades_temario
            WHERE veces_visto = 0 {and_clause}
            ORDER BY RANDOM()
            LIMIT 1
            """,
            params_base,
        )
        row = cur.fetchone()
        if row:
            conn.close()
            return {
                "unidad": dict(row),
                "es_refuerzo": 0,
                "motivo_seleccion": f"Simulacro Global: Evaluando precepto aleatorio de {row['documento'][:30]}...",
            }
    else:
        # Cobertura 100% garantizada con rotación ordenada entre los PDFs (Piloto Automático clásico)
        cur.execute(
            f"""
            SELECT documento, SUM(veces_visto) as total_vistos_doc
            FROM unidades_temario
            WHERE veces_visto = 0 {and_clause}
            GROUP BY documento
            ORDER BY total_vistos_doc ASC, documento ASC
            LIMIT 1
            """,
            params_base,
        )
        doc_menos_visto = cur.fetchone()
        if doc_menos_visto:
            cur.execute(
                """
                SELECT * FROM unidades_temario
                WHERE veces_visto = 0 AND documento = ?
                ORDER BY id ASC
                LIMIT 1
                """,
                (doc_menos_visto["documento"],),
            )
            row = cur.fetchone()
            if row:
                conn.close()
                return {
                    "unidad": dict(row),
                    "es_refuerzo": 0,
                    "motivo_seleccion": f"Estudio Secuencial: Siguiente precepto de {row['documento'][:42]}...",
                }

    # 4. Repaso espaciado vencido o escalada pendiente
    if filtro_documento == "SIMULACRO_GLOBAL":
        cur.execute(
            f"""
            SELECT * FROM unidades_temario
            WHERE (dominio_score < 85 OR proximo_repaso <= ?) {and_clause}
            ORDER BY RANDOM()
            LIMIT 1
            """,
            [ahora_iso, *params_base],
        )
        row = cur.fetchone()
        if row:
            conn.close()
            return {
                "unidad": dict(row),
                "es_refuerzo": 0,
                "motivo_seleccion": f"Simulacro Global: Evaluando repaso espaciado de {row['documento'][:30]}...",
            }
    else:
        cur.execute(
            f"""
            SELECT * FROM unidades_temario
            WHERE (dominio_score < 85 OR proximo_repaso <= ?) {and_clause}
            ORDER BY dominio_score ASC, veces_visto ASC
            LIMIT 1
            """,
            [ahora_iso, *params_base],
        )
        row = cur.fetchone()
        if row:
            conn.close()
            return {
                "unidad": dict(row),
                "es_refuerzo": 0,
                "motivo_seleccion": f"Escalada / Repetición Espaciada: Evaluando Nivel {row['nivel_actual']}.",
            }

    cur.execute(
        f"SELECT * FROM unidades_temario {where_base} ORDER BY RANDOM() LIMIT 1",
        params_base,
    )
    row = cur.fetchone()
    conn.close()
    return {
        "unidad": dict(row),
        "es_refuerzo": 0,
        "motivo_seleccion": "Repaso General de Maestría ADIF.",
    }


def _buscar_recurso_estilo(nombre: str) -> Path | None:
    """Busca un fichero de estilo junto a la app o en la carpeta estilo/ del repositorio."""
    for candidato in (BASE_DIR / nombre, BASE_DIR / "estilo" / nombre, BASE_DIR.parent / "estilo" / nombre):
        if candidato.exists():
            return candidato
    return None


def _cargar_guia_estilo() -> str:
    ruta = _buscar_recurso_estilo("adn_tribunal.md")
    if not ruta:
        return "No disponible."
    texto = ruta.read_text(encoding="utf-8")
    # Solo las secciones normativas; los ejemplos ya van aparte en el prompt
    corte = texto.find("## Ejemplos reales")
    return texto[:corte].strip() if corte != -1 else texto.strip()


def _normalizar_texto(texto: str) -> str:
    return re.sub(r"\s+", " ", norm_nfc(texto)).strip().lower()


def _clave_norma(documento: str) -> str | None:
    """'02 Ley 47_2003, de 26 de...' -> '47/2003'; sirve para buscar preguntas oficiales de la misma norma."""
    m = re.search(r"(\d{1,4})[_/\-](\d{4})", documento)
    return f"{m.group(1)}/{m.group(2)}" if m else None


def _ejemplos_tribunal_para(cur: sqlite3.Cursor, documento: str, total: int = 4) -> list[dict[str, Any]]:
    """Prioriza preguntas oficiales de la misma norma y completa con preguntas oficiales al azar."""
    ejemplos: list[dict[str, Any]] = []
    clave = _clave_norma(documento)
    if clave:
        cur.execute(
            "SELECT id, documento_origen, enunciado, patron_trampa FROM adn_tribunal "
            "WHERE enunciado LIKE ? ORDER BY documento_origen LIKE 'OFICIAL%' DESC, RANDOM()",
            (f"%{clave}%",),
        )
        # El LIKE de «8/2015» también encuentra «38/2015»: se filtra con límite de número
        exacta = re.compile(rf"(?<!\d){re.escape(clave)}")
        ejemplos = [dict(r) for r in cur.fetchall() if exacta.search(r["enunciado"])][:total]
    if len(ejemplos) < total:
        ya = [e["id"] for e in ejemplos] or [-1]
        cur.execute(
            f"SELECT id, documento_origen, enunciado, patron_trampa FROM adn_tribunal "
            f"WHERE id NOT IN ({','.join('?' * len(ya))}) "
            "ORDER BY documento_origen LIKE 'OFICIAL%' DESC, RANDOM() LIMIT ?",
            (*ya, total - len(ejemplos)),
        )
        ejemplos += [dict(r) for r in cur.fetchall()]
    return ejemplos


def _motivo_rechazo_pregunta(data: dict[str, Any], contenido_literal: str) -> str | None:
    """Control de calidad de una pregunta generada. Devuelve el motivo de rechazo o None si es válida."""
    opciones = data.get("opciones")
    indice = data.get("indice_correcta")
    if not isinstance(opciones, list) or len(opciones) != 4 or not all(isinstance(o, str) and o.strip() for o in opciones):
        return "no tiene 4 opciones"
    if not isinstance(indice, int) or not 0 <= indice < 4:
        return "indice_correcta inválido"
    if len({_normalizar_texto(o) for o in opciones}) < 4:
        return "opciones repetidas"

    # La cita debe estar copiada del precepto (se admiten varios fragmentos separados por […] o ...)
    cita = re.sub(r"^[\"«“\s]+|[\"»”\s]+$", "", data.get("cita_literal_boe", ""))
    fuente = _normalizar_texto(contenido_literal)
    fragmentos = [f for f in re.split(r"\s*(?:\[…\]|\[\.\.\.\]|…|\.\.\.)\s*", cita) if len(f) > 15]
    if not fragmentos or any(_normalizar_texto(f).strip("\"«»“” ") not in fuente for f in fragmentos):
        return "cita_literal_boe no aparece en el texto del precepto"

    enunciado = _normalizar_texto(data.get("enunciado", ""))
    correcta = _normalizar_texto(opciones[indice]).rstrip(".")
    if len(correcta) > 25 and correcta in enunciado:
        return "el enunciado revela la respuesta"

    # Una correcta desproporcionadamente larga regala la respuesta
    largo_distractores = max(len(o) for i, o in enumerate(opciones) if i != indice)
    if len(opciones[indice]) > 2.5 * largo_distractores and len(opciones[indice]) > 80:
        return "la opción correcta es mucho más larga que los distractores"
    return None


def cargar_ejemplos_oficiales() -> int:
    """Carga en adn_tribunal las preguntas oficiales de estilo/ejemplos.json (con su respuesta de plantilla)."""
    ruta = _buscar_recurso_estilo("ejemplos.json")
    if not ruta:
        return 0
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM adn_tribunal WHERE documento_origen LIKE 'OFICIAL%'")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 0

    nuevos = 0
    for p in json.loads(ruta.read_text(encoding="utf-8")):
        if not p.get("correcta"):
            continue
        indice = "ABCD".index(p["correcta"])
        texto = p["enunciado"] + "\n" + "\n".join(
            f"{'abcd'[i]}) {o}" for i, o in enumerate(p["opciones"])
        ) + f"\nRespuesta oficial: {p['correcta']}"
        negativa = bool(re.search(r"\bNO\b|INCORRECTA", p["enunciado"]))
        patron = (
            "Formulación negativa: tres opciones literales de la enumeración legal y una ajena verosímil."
            if negativa
            else f"Correcta: «{p['opciones'][indice]}». Los distractores mantienen la estructura y cambian cifra, órgano o ámbito."
        )
        cur.execute(
            "INSERT INTO adn_tribunal (documento_origen, enunciado, patron_trampa) VALUES (?, ?, ?)",
            (f"OFICIAL {p['convocatoria']} - examen {p.get('codigo_examen') or 's/c'} - n.º {p['numero']}", texto, patron),
        )
        nuevos += 1
    conn.commit()
    conn.close()
    return nuevos


def generar_pregunta_con_gemini(unidad: dict[str, Any], es_refuerzo: int) -> dict[str, Any] | None:
    """
    Genera en vivo una pregunta calcada al estilo del Tribunal de ADIF (PNI26/03)
    usando `gemini-3-flash-preview` (con respaldo en `gemini-2.5-flash-lite`),
    el texto literal del PDF de la carpeta APP y ejemplos reales de los exámenes 2021-2025.
    Garantiza además no repetir ninguna pregunta previa hecha sobre esa misma unidad.
    """
    api_key = obtener_api_key()
    if not api_key:
        return None

    conn = get_db_connection()
    cur = conn.cursor()
    ejemplos_tribunal = _ejemplos_tribunal_para(cur, unidad["documento"])

    cur.execute("SELECT enunciado FROM banco_preguntas WHERE unidad_id = ?", (unidad["id"],))
    preguntas_previas = [r["enunciado"] for r in cur.fetchall()]
    conn.close()

    ejemplos_txt = "\n\n".join(
        f"[{e['documento_origen']}]\n{e['enunciado']}\nPatrón del Tribunal ADIF: {e['patron_trampa']}"
        for e in ejemplos_tribunal
    )

    previas_txt = (
        "\n".join(f"- {enun}" for enun in preguntas_previas)
        if preguntas_previas
        else "Ninguna todavía."
    )

    nivel = unidad["nivel_actual"]
    descripciones_nivel = {
        1: "NIVEL 1 (Literalidad de Examen ADIF): Evalúa la regla principal, plazo o definición del artículo con 4 opciones formales donde solo 1 es exacta.",
        2: "NIVEL 2 (Trampa Quirúrgica estilo ADIF): Usa el patrón típico de ADIF: 4 opciones muy parecidas (o pregunta 'Señale la opción INCORRECTA') donde los distractores cambian 'salvo que' por 'en los casos en que', plazos (1 mes vs 3 meses), o 'podrá' por 'deberá'.",
        3: "NIVEL 3 (Excepción / Supuesto Complejo ADIF): Pregunta por la excepción del precepto, el cómputo exacto de plazos o un supuesto aplicado a la entidad pública empresarial ADIF.",
    }

    instruccion_rama = (
        f"MODO RAMA DE REFUERZO OBLIGATORIO: El opositor acaba de FALLAR este artículo debido a: '{unidad.get('ultimo_error_detalle') or unidad.get('ultimo_error_tipo') or 'confusión en el precepto'}'. "
        "Formula una pregunta totalmente NUEVA sobre este mismo precepto desde otro ángulo para verificar que ya no cae en esa trampa del Tribunal."
        if es_refuerzo
        else descripciones_nivel.get(nivel, descripciones_nivel[1])
    )

    prompt = f"""Eres el Tribunal de Evaluación de la Convocatoria Pública de Ingreso en ADIF (OEP 2026 - Código PNI26/03).
Redacta UNA pregunta oficial tipo test con 4 opciones de respuesta (solo 1 correcta) basada EXCLUSIVAMENTE en el siguiente precepto literal extraído del PDF del opositor:

=== FUENTE OFICIAL DEL TEMARIO ADIF 2026 ===
Bloque: {unidad['bloque_temario']}
Documento PDF: {unidad['documento']}
Precepto / Apartado: {unidad['titulo_unidad']}
Texto literal:
{unidad['contenido_literal']}

=== GUÍA DE ESTILO DEL TRIBUNAL ADIF (análisis de 559 preguntas oficiales 2022-2025) ===
{_cargar_guia_estilo()}

=== PREGUNTAS REALES DE EXÁMENES ANTERIORES DE ADIF COMO MOLDE DE ESTILO ===
{ejemplos_txt}

=== PREGUNTAS YA REALIZADAS SOBRE ESTE ARTÍCULO (PROHIBIDO REPETIRLAS O PARAFRASEARLAS) ===
{previas_txt}

=== DIRECTRIZ DEL MOTOR ADAPTATIVO ===
{instruccion_rama}

REGLAS DE FIABILIDAD ABSOLUTA (CERO ALUCINACIONES):
1. No inventes ningún dato que no figure literalmente en el Texto literal de arriba.
2. En `cita_literal_boe`, escribe ÚNICAMENTE la frase o frases EXACTAS copiadas y pegadas del 'Texto literal' que respaldan tu respuesta. No uses tus propias palabras, no resumas y no añadas introducciones como 'El artículo dice que'. Usa comillas " ".
3. En `trampas_por_opcion` (array de 4 textos), detalla para cada opción (A, B, C, D) qué palabra o plazo se ha alterado como trampa del Tribunal o por qué es la correcta.
4. PROHIBIDO preguntar por derogaciones normativas, disposiciones derogatorias, qué leyes o reglamentos antiguos quedan derogados o si un apartado fue derogado/suprimido. Pregunta SIEMPRE por el contenido material y sustantivo vigente del precepto (competencias, plazos, definiciones, derechos, obligaciones, órganos o procedimientos).
5. EL ENUNCIADO NO DEBE REVELAR LA RESPUESTA. Es un error gravísimo copiar el artículo entero o la respuesta correcta dentro del enunciado. El enunciado debe ser una pregunta directa corta (ej. "¿En qué consideraciones se fundamentará la actuación de los empleados públicos según el art. 53...?") o una frase a completar (ej. "Según el artículo 53..., la actuación de los empleados públicos se fundamentará en:").
6. MUY IMPORTANTE: En la `explicacion_detallada` y en `trampas_por_opcion`, NUNCA menciones las letras de las opciones (es decir, NO digas "La respuesta correcta es la A", ni "La opción B es falsa"). Las opciones se van a barajar aleatoriamente después de que las generes. Refiérete siempre al contenido ("La respuesta correcta es la que indica que...").

Devuelve ÚNICAMENTE un JSON válido con este esquema:
{{
  "trampa_objetivo": "Resumen corto de qué evalúa la pregunta",
  "enunciado": "Enunciado formal estilo examen ADIF...",
  "opciones": ["Texto opción A", "Texto opción B", "Texto opción C", "Texto opción D"],
  "indice_correcta": 0,
  "cita_literal_boe": "Cita literal entrecomillada del documento...",
  "explicacion_detallada": "Explicación clara para el opositor...",
  "trampas_por_opcion": ["Análisis A", "Análisis B", "Análisis C", "Análisis D"]
}}
"""

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    for modelo_nombre in MODELOS_GEMINI_ACTIVOS:
        try:
            response = client.models.generate_content(
                model=modelo_nombre,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )
            if not response.text:
                continue
            data = json.loads(response.text)
            if _motivo_rechazo_pregunta(data, unidad["contenido_literal"]) is None:
                import random
                
                opciones_orig = data["opciones"]
                indice_orig = data["indice_correcta"]
                trampas_orig = data.get("trampas_por_opcion", ["", "", "", ""])
                
                # Emparejar para barajar manteniendo la coherencia
                pares = list(zip(opciones_orig, trampas_orig))
                # Guardar la referencia al par correcto antes de barajar
                par_correcto = pares[indice_orig] if 0 <= indice_orig < 4 else pares[0]
                
                random.shuffle(pares)
                
                # Desempaquetar y actualizar los índices
                data["opciones"] = [p[0] for p in pares]
                data["trampas_por_opcion"] = [p[1] for p in pares]
                data["indice_correcta"] = pares.index(par_correcto)

                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO banco_preguntas (
                        unidad_id, nivel, es_refuerzo, trampa_objetivo, enunciado,
                        opciones_json, indice_correcta, cita_literal_boe,
                        explicacion_detallada, trampas_por_opcion_json, usada
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        unidad["id"],
                        nivel,
                        es_refuerzo,
                        data.get("trampa_objetivo", f"Evaluación ADIF ({modelo_nombre})"),
                        data["enunciado"],
                        json.dumps(data["opciones"], ensure_ascii=False),
                        data["indice_correcta"],
                        data.get("cita_literal_boe", ""),
                        data.get("explicacion_detallada", ""),
                        json.dumps(data.get("trampas_por_opcion", ["", "", "", ""]), ensure_ascii=False),
                    ),
                )
                pregunta_id = cur.lastrowid
                conn.commit()
                cur.execute("SELECT * FROM banco_preguntas WHERE id = ?", (pregunta_id,))
                row = dict(cur.fetchone())
                conn.close()
                return row
        except Exception:
            continue

    return None


def obtener_siguiente_pregunta(filtro_bloque: str = "PERFIL_GESTION", filtro_documento: str = "TODOS") -> dict[str, Any]:
    objetivo = seleccionar_siguiente_objetivo(filtro_bloque, filtro_documento)
    unidad = objetivo["unidad"]
    es_refuerzo = objetivo["es_refuerzo"]
    nivel = unidad["nivel_actual"]

    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Buscar exclusivamente preguntas NO USADAS (usada = 0) para esa unidad, nivel y modo refuerzo
    cur.execute(
        """
        SELECT * FROM banco_preguntas
        WHERE unidad_id = ? AND nivel = ? AND es_refuerzo = ? AND usada = 0
        ORDER BY id ASC LIMIT 1
        """,
        (unidad["id"], nivel, es_refuerzo),
    )
    pregunta_row = cur.fetchone()

    if pregunta_row:
        pregunta = dict(pregunta_row)
        conn.close()
    else:
        conn.close()
        # 2. Generar pregunta NUEVA en vivo con Gemini 3 Flash / 2.5 Flash Lite
        generada = generar_pregunta_con_gemini(unidad, es_refuerzo)
        if generada:
            pregunta = generada
        else:
            # 3. Si no hubiera internet/API, buscar solo preguntas NO USADAS (usada = 0) en el banco
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM banco_preguntas WHERE usada = 0 ORDER BY id ASC LIMIT 1"
            )
            fallback = cur.fetchone()
            if not fallback:
                cur.execute("SELECT * FROM banco_preguntas ORDER BY RANDOM() LIMIT 1")
                fallback = cur.fetchone()
            pregunta = dict(fallback)
            cur.execute("SELECT * FROM unidades_temario WHERE id = ?", (pregunta["unidad_id"],))
            unidad = dict(cur.fetchone())
            conn.close()

    return {
        "pregunta_id": pregunta["id"],
        "unidad_id": unidad["id"],
        "bloque_temario": unidad["bloque_temario"],
        "documento": unidad["documento"],
        "codigo_unidad": unidad["codigo_unidad"],
        "titulo_unidad": unidad["titulo_unidad"],
        "nivel": pregunta["nivel"],
        "es_refuerzo": bool(pregunta["es_refuerzo"]),
        "trampa_objetivo": pregunta["trampa_objetivo"],
        "motivo_seleccion": objetivo["motivo_seleccion"],
        "dominio_actual": round(unidad["dominio_score"], 1),
        "enunciado": pregunta["enunciado"],
        "opciones": json.loads(pregunta["opciones_json"]),
        "tiene_api_key": bool(obtener_api_key()),
    }


def registrar_respuesta_y_ramificar(pregunta_id: int, opcion_elegida: int) -> dict[str, Any]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM banco_preguntas WHERE id = ?", (pregunta_id,))
    pregunta = dict(cur.fetchone())
    unidad_id = pregunta["unidad_id"]

    cur.execute("SELECT * FROM unidades_temario WHERE id = ?", (unidad_id,))
    unidad = dict(cur.fetchone())

    indice_correcta = pregunta["indice_correcta"]
    es_blanco = opcion_elegida < 0
    acierto = 1 if (not es_blanco and opcion_elegida == indice_correcta) else 0
    trampas_opciones = json.loads(pregunta["trampas_por_opcion_json"])
    analisis_eleccion = (
        "Pregunta dejada en blanco (0 puntos, no penaliza -1/3 según Bases ADIF)."
        if es_blanco
        else (
            trampas_opciones[opcion_elegida]
            if 0 <= opcion_elegida < len(trampas_opciones)
            else ""
        )
    )

    nivel_anterior = unidad["nivel_actual"]
    dominio_anterior = unidad["dominio_score"]
    ahora = datetime.datetime.now()

    if acierto:
        nueva_racha = unidad["racha_aciertos"] + 1
        nuevo_dominio = min(100.0, dominio_anterior + (30.0 if nivel_anterior < 3 else 25.0))
        prioridad_refuerzo = 0

        if pregunta["es_refuerzo"]:
            nuevo_nivel = min(3, max(1, nivel_anterior) + 1)
            intervalo_dias = 1
            accion_motor = (
                f"Refuerzo superado en {unidad['codigo_unidad']}. "
                f"Salimos de la rama correctiva y escalamos a Nivel {nuevo_nivel}."
            )
        elif nivel_anterior == 1:
            nuevo_nivel = 2
            intervalo_dias = 1
            accion_motor = (
                f"¡Acierto en Nivel 1! El motor sube {unidad['codigo_unidad']} a "
                "NIVEL 2 (Trampas quirúrgicas de Tribunal ADIF)."
            )
        elif nivel_anterior == 2:
            nuevo_nivel = 3
            intervalo_dias = 3
            accion_motor = (
                f"¡Acierto en Nivel 2! El motor sube {unidad['codigo_unidad']} a "
                "NIVEL 3 (Excepciones y casos complejos ADIF)."
            )
        else:
            nuevo_nivel = 3
            intervalo_dias = max(7, (unidad["intervalo_dias"] or 3) * 2)
            accion_motor = (
                f"¡Dominio Nivel 3 consolidado en {unidad['codigo_unidad']}! "
                f"Precepto dominado: próximo repaso espaciado en {intervalo_dias} días."
            )

        proximo_repaso = (ahora + datetime.timedelta(days=intervalo_dias)).isoformat()
        ultimo_error_tipo = unidad["ultimo_error_tipo"]
        ultimo_error_detalle = unidad["ultimo_error_detalle"]
    elif es_blanco:
        nueva_racha = 0
        nuevo_dominio = dominio_anterior
        nuevo_nivel = nivel_anterior
        prioridad_refuerzo = 0
        intervalo_dias = 0
        proximo_repaso = (ahora + datetime.timedelta(hours=12)).isoformat()
        ultimo_error_tipo = "Pregunta dejada en blanco"
        ultimo_error_detalle = pregunta["trampa_objetivo"]
        accion_motor = (
            f"Dejada en blanco en {unidad['codigo_unidad']}: no resta puntos en tu nota ADIF. "
            "Queda pendiente para repaso posterior."
        )
    else:
        nueva_racha = 0
        nuevo_dominio = max(0.0, dominio_anterior - 20.0)
        nuevo_nivel = max(1, nivel_anterior - 1)
        prioridad_refuerzo = 1
        intervalo_dias = 0
        proximo_repaso = ahora.isoformat()
        ultimo_error_tipo = pregunta["trampa_objetivo"]
        ultimo_error_detalle = analisis_eleccion
        accion_motor = (
            f"Fallo en {unidad['codigo_unidad']} ({pregunta['trampa_objetivo']}). "
            "Se activa la RAMA DE REFUERZO: tu siguiente pregunta volverá a evaluar este artículo con una pregunta nueva desde otro ángulo."
        )

    cur.execute("UPDATE banco_preguntas SET usada = 1 WHERE id = ?", (pregunta_id,))
    cur.execute(
        """
        UPDATE unidades_temario
        SET nivel_actual = ?,
            dominio_score = ?,
            veces_visto = veces_visto + 1,
            aciertos_totales = aciertos_totales + ?,
            fallos_totales = fallos_totales + ?,
            racha_aciertos = ?,
            prioridad_refuerzo = ?,
            ultimo_error_tipo = ?,
            ultimo_error_detalle = ?,
            intervalo_dias = ?,
            proximo_repaso = ?
        WHERE id = ?
        """,
        (
            nuevo_nivel,
            nuevo_dominio,
            1 if acierto else 0,
            0 if (acierto or es_blanco) else 1,
            nueva_racha,
            prioridad_refuerzo,
            ultimo_error_tipo,
            ultimo_error_detalle,
            intervalo_dias,
            proximo_repaso,
            unidad_id,
        ),
    )

    cur.execute(
        """
        INSERT INTO historial_respuestas (
            unidad_id, pregunta_id, nivel_pregunta, es_refuerzo,
            opcion_elegida, acierto, trampa_caida, accion_motor, fecha
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            unidad_id,
            pregunta_id,
            pregunta["nivel"],
            pregunta["es_refuerzo"],
            opcion_elegida,
            acierto,
            "EN BLANCO" if es_blanco else ("" if acierto else pregunta["trampa_objetivo"]),
            accion_motor,
            ahora.isoformat(),
        ),
    )

    conn.commit()
    conn.close()

    return {
        "acierto": bool(acierto),
        "es_blanco": es_blanco,
        "indice_correcta": indice_correcta,
        "opcion_elegida": opcion_elegida,
        "cita_literal_boe": pregunta["cita_literal_boe"],
        "explicacion_detallada": pregunta["explicacion_detallada"],
        "trampas_por_opcion": trampas_opciones,
        "analisis_tu_eleccion": analisis_eleccion,
        "ramificacion": {
            "nivel_anterior": nivel_anterior,
            "nuevo_nivel": nuevo_nivel,
            "dominio_anterior": round(dominio_anterior, 1),
            "nuevo_dominio": round(nuevo_dominio, 1),
            "prioridad_refuerzo_activada": bool(prioridad_refuerzo),
            "accion_motor": accion_motor,
        },
    }


def obtener_estado_global(filtro_bloque: str = "PERFIL_GESTION", filtro_documento: str = "TODOS") -> dict[str, Any]:
    conn = get_db_connection()
    cur = conn.cursor()

    where_sql, params = construir_filtro_sql(filtro_bloque, filtro_documento)

    cur.execute(
        f"""
        SELECT 
            bloque_temario, 
            documento,
            AVG(dominio_score) as dominio_score,
            COUNT(*) as total_articulos,
            SUM(CASE WHEN veces_visto > 0 THEN 1 ELSE 0 END) as veces_visto,
            SUM(CASE WHEN dominio_score >= 80.0 THEN 1 ELSE 0 END) as dominadas,
            SUM(aciertos_totales) as aciertos_totales,
            SUM(fallos_totales) as fallos_totales,
            SUM(prioridad_refuerzo) as prioridad_refuerzo
        FROM unidades_temario
        {where_sql}
        GROUP BY bloque_temario, documento
        ORDER BY bloque_temario ASC, documento ASC
        """,
        params,
    )
    unidades = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT bloque_temario, documento FROM unidades_temario ORDER BY bloque_temario ASC, documento ASC")
    documentos_disponibles = [dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN acierto = 1 THEN 1 ELSE 0 END) as aciertos,
            SUM(CASE WHEN opcion_elegida < 0 THEN 1 ELSE 0 END) as blancos,
            SUM(CASE WHEN acierto = 0 AND opcion_elegida >= 0 THEN 1 ELSE 0 END) as fallos
        FROM historial_respuestas
        """
    )
    stats_row = cur.fetchone()
    total_respuestas = stats_row["total"] or 0
    aciertos = stats_row["aciertos"] or 0
    blancos = stats_row["blancos"] or 0
    fallos = stats_row["fallos"] or 0

    # Fórmula oficial ADIF (Bases PNI26/03): Aciertos - (Errores / 3); las respuestas en blanco ni puntúan ni penalizan
    puntos_netos = max(0.0, aciertos - (fallos / 3.0))
    nota_sobre_120 = round((puntos_netos / total_respuestas) * 120.0, 1) if total_respuestas > 0 else 0.0
    nota_sobre_10 = round((puntos_netos / total_respuestas) * 10.0, 2) if total_respuestas > 0 else 0.0

    total_unidades = sum(u["total_articulos"] for u in unidades)
    unidades_vistas = sum(u["veces_visto"] for u in unidades)
    unidades_dominadas = sum(u["dominadas"] for u in unidades)
    unidades_en_alerta = sum(u["prioridad_refuerzo"] for u in unidades)
    cobertura_pct = round((unidades_vistas / total_unidades) * 100.0, 1) if total_unidades > 0 else 0.0

    cur.execute("SELECT COUNT(*) FROM adn_tribunal")
    patrones_tribunal = cur.fetchone()[0]

    cur.execute(
        """
        SELECT h.*, u.codigo_unidad, u.documento
        FROM historial_respuestas h
        JOIN unidades_temario u ON u.id = h.unidad_id
        ORDER BY h.id DESC LIMIT 8
        """
    )
    ultimas_decisiones = [dict(r) for r in cur.fetchall()]

    conn.close()

    return {
        "resumen": {
            "total_unidades": total_unidades,
            "unidades_vistas": unidades_vistas,
            "unidades_dominadas": unidades_dominadas,
            "unidades_en_alerta": unidades_en_alerta,
            "cobertura_pct": cobertura_pct,
            "total_respuestas": total_respuestas,
            "aciertos": aciertos,
            "fallos": fallos,
            "blancos": blancos,
            "nota_adif_sobre_120": nota_sobre_120,
            "nota_oposicion_sobre_10": nota_sobre_10,
            "supera_corte_40_pct": nota_sobre_120 >= 48.0 if total_respuestas > 0 else False,
            "patrones_tribunal_cargados": patrones_tribunal,
            "tiene_api_key": bool(obtener_api_key()),
        },
        "documentos_disponibles": documentos_disponibles,
        "unidades": unidades[:250],
        "ultimas_decisiones": ultimas_decisiones,
    }


def depurar_unidades_y_preguntas_derogacion() -> dict[str, int]:
    """
    Limpia de la base de datos:
    1. Decretos envoltorio ('Artículo único. Aprobación del texto refundido...') que contienen la Disposición derogatoria única.
    2. Artículos cuyo texto es únicamente '(Derogado)', '(Suprimido)' o 'Derogación'.
    3. Disposiciones derogatorias/finales pegadas al final del último artículo de una ley.
    4. Cualquier pregunta generada en banco_preguntas que pregunte por derogaciones.
    """
    if not DB_PATH.exists():
        return {"unidades_eliminadas": 0, "preguntas_eliminadas": 0}

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, contenido_literal FROM unidades_temario")
    rows = cur.fetchall()
    ids_eliminar: list[int] = []

    for r in rows:
        uid = r["id"]
        txt_original = r["contenido_literal"]
        txt_limpio = re.split(
            r"(?m)^Disposici[oó]n\s+(?:derogatoria|final|transitoria)\b",
            txt_original,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0].strip()

        if not _es_fragmento_valido(txt_limpio):
            ids_eliminar.append(uid)
        elif txt_limpio != txt_original:
            cur.execute(
                "UPDATE unidades_temario SET contenido_literal = ? WHERE id = ?",
                (txt_limpio, uid),
            )

    if ids_eliminar:
        placeholders = ",".join("?" for _ in ids_eliminar)
        cur.execute(f"DELETE FROM historial_respuestas WHERE unidad_id IN ({placeholders})", ids_eliminar)
        cur.execute(f"DELETE FROM banco_preguntas WHERE unidad_id IN ({placeholders})", ids_eliminar)
        cur.execute(f"DELETE FROM unidades_temario WHERE id IN ({placeholders})", ids_eliminar)

    # Eliminar cualquier pregunta en banco_preguntas que pregunte sobre derogaciones o artículos suprimidos
    cur.execute(
        """
        SELECT id FROM banco_preguntas
        WHERE lower(enunciado) LIKE '%derog%'
           OR lower(enunciado) LIKE '%suprimid%'
           OR lower(cita_literal_boe) LIKE '%queda derogado%'
           OR lower(cita_literal_boe) LIKE '%quedan derogad%'
        """
    )
    q_ids = [r["id"] for r in cur.fetchall()]
    if q_ids:
        q_placeholders = ",".join("?" for _ in q_ids)
        cur.execute(f"DELETE FROM historial_respuestas WHERE pregunta_id IN ({q_placeholders})", q_ids)
        cur.execute(f"DELETE FROM banco_preguntas WHERE id IN ({q_placeholders})", q_ids)

    conn.commit()
    conn.close()
    return {"unidades_eliminadas": len(ids_eliminar), "preguntas_eliminadas": len(q_ids)}


try:
    depurar_unidades_y_preguntas_derogacion()
except Exception:
    pass

