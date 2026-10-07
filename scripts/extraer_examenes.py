"""
Extrae las preguntas reales de los cuadernillos oficiales de ADIF (2022-2025) y las cruza
con sus plantillas correctoras. Genera estilo/ejemplos.json, que sirve de corpus de estilo
del Tribunal y alimenta la tabla adn_tribunal de la app.

Uso:
    python scripts/extraer_examenes.py ex2025.pdf:2025 ex2024.pdf:2024 ... -o estilo/ejemplos.json

Los cuadernillos vienen maquetados a dos columnas, así que cada página se recorta en
mitad izquierda y derecha antes de extraer el texto (pdftotext lo intercala).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pdfplumber

RE_CODIGO = re.compile(r"C[óo]digo (?:de ex[áa]men|del libro):?\s*(\d{4})")
RE_PREGUNTA = re.compile(r"^(\d{1,3})\.\s*(.*)$")
RE_OPCION = re.compile(r"^([a-dA-D])[\)\.]\s*(.*)$")
RE_TEMARIO = re.compile(
    r"¿|\b(Ley|Real Decreto|RD|LO|Reglamento|Adif|ADIF|LCSP|ENS|Estatuto|Declaraci[óo]n|Orden|Canal|Informe|"
    r"Seguridad Social|Administraci[óo]n|empresario|trabajador)"
)
RUIDO = re.compile(
    r"^(P[áa]gina \d+|Reserva.*|Conocimientos?|Conocimentos|Conocimiento (General|Espec[íi]fico)|"
    r"Ingl[ée]s|Franc[ée]s|TEST DE CONOCIMIENTOS|NO ABRA.*)$"
)


# Plantillas publicadas como página girada (pdfplumber no las lee como tabla).
# Transcritas del PDF oficial PNI25/02, Cuadro Técnico - Área Gestión (25/19CT).
PLANTILLAS_MANUALES = {
    "3214": "BCDADCCCADBCCBABAD",
    "4004": "CCCBDCADABCADCBDCC",
}


def leer_plantillas(pdf) -> dict[str, dict[int, str]]:
    """{codigo_examen: {numero: letra}} a partir de las tablas de plantillas correctoras."""
    plantillas: dict[str, dict[int, str]] = {
        cod: {i + 1: letra for i, letra in enumerate(letras)} for cod, letras in PLANTILLAS_MANUALES.items()
    }
    for page in pdf.pages:
        for tabla in page.extract_tables():
            codigos: list[str | None] = []
            for fila in tabla:
                celdas = [(c or "").strip() for c in fila]
                if any(re.match(r"C[óo]digo (de ex|del libro)", c) for c in celdas):
                    codigos = [celdas[i + 1] if i + 1 < len(celdas) and re.fullmatch(r"\d{4}", celdas[i + 1]) else None
                               for i, c in enumerate(celdas) if re.match(r"C[óo]digo (de ex|del libro)", c)]
                    for cod in codigos:
                        if cod:
                            plantillas.setdefault(cod, {})
                    continue
                if not codigos:
                    continue
                pares = [(celdas[i], celdas[i + 1]) for i in range(0, len(celdas) - 1, 2)]
                for cod, (num, letra) in zip(codigos, pares):
                    if cod and num.isdigit() and re.fullmatch(r"[A-D]", letra):
                        plantillas[cod][int(num)] = letra
    return plantillas


def texto_por_columnas(page) -> str:
    mitad = page.width / 2
    izq = page.crop((0, 0, mitad, page.height)).extract_text() or ""
    der = page.crop((mitad, 0, page.width, page.height)).extract_text() or ""
    return izq + "\n" + der


def parsear_preguntas(lineas: list[str]) -> list[dict]:
    preguntas: list[dict] = []
    actual: dict | None = None
    for linea in lineas:
        s = linea.strip()
        if not s or RUIDO.match(s):
            continue
        m_p = RE_PREGUNTA.match(s)
        m_o = RE_OPCION.match(s)
        if m_p and (actual is None or len(actual["opciones"]) == 4 or not actual["opciones"]):
            if actual is None or len(actual["opciones"]) == 4:
                actual = {"numero": int(m_p.group(1)), "enunciado": m_p.group(2), "opciones": []}
                preguntas.append(actual)
                continue
        if actual is None:
            continue
        if m_o and m_o.group(1).lower() == "abcd"[len(actual["opciones"]) % 4] and len(actual["opciones"]) < 4:
            actual["opciones"].append(m_o.group(2))
        elif actual["opciones"]:
            actual["opciones"][-1] += " " + s
        else:
            actual["enunciado"] += " " + s
    return [p for p in preguntas if len(p["opciones"]) == 4]


def extraer(pdf_path: Path, convocatoria: str) -> list[dict]:
    resultado: list[dict] = []
    with pdfplumber.open(pdf_path) as pdf:
        plantillas = leer_plantillas(pdf)
        cuadernillos: list[tuple[str | None, list[str]]] = []
        for page in pdf.pages:
            texto_plano = page.extract_text() or ""
            if re.search(r"Respuesta correcta|CUADERNILLOS DE EXAMEN|PUBLICACI[ÓO]N DE PLANTILLAS", texto_plano):
                continue
            m_cod = RE_CODIGO.search(texto_plano)
            if m_cod and "INSTRUCCIONES" in texto_plano.upper():
                cuadernillos.append((m_cod.group(1), []))
                continue
            if not cuadernillos:
                cuadernillos.append((None, []))
            cuadernillos[-1][1].extend(texto_por_columnas(page).splitlines())

        vistos: set[str] = set()
        for codigo, lineas in cuadernillos:
            respuestas = plantillas.get(codigo or "", {})
            for p in parsear_preguntas(lineas):
                enunciado = re.sub(r"\s+", " ", p["enunciado"]).strip()
                # Restos del pie "Conocimiento Específico" partido por el recorte de columnas
                opciones = [re.sub(r"\s+(?:í?fico|ico)$", "", re.sub(r"\s+", " ", o).strip()) for o in p["opciones"]]
                # Inglés/francés y psicotécnicos no aportan al estilo de temario
                if "____" in enunciado or not RE_TEMARIO.search(enunciado + " " + " ".join(opciones)):
                    continue
                clave = enunciado.lower()
                if clave in vistos:
                    continue
                vistos.add(clave)
                letra = respuestas.get(p["numero"])
                resultado.append(
                    {
                        "convocatoria": convocatoria,
                        "codigo_examen": codigo,
                        "numero": p["numero"],
                        "enunciado": enunciado,
                        "opciones": opciones,
                        "correcta": letra,
                    }
                )
    return resultado


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("entradas", nargs="+", help="ruta.pdf:convocatoria")
    ap.add_argument("-o", "--salida", default="estilo/ejemplos.json")
    args = ap.parse_args()

    todas: list[dict] = []
    for entrada in args.entradas:
        ruta, _, conv = entrada.rpartition(":")
        preguntas = extraer(Path(ruta), conv)
        con_resp = sum(1 for p in preguntas if p["correcta"])
        print(f"{conv}: {len(preguntas)} preguntas ({con_resp} con respuesta oficial)", file=sys.stderr)
        todas.extend(preguntas)

    Path(args.salida).write_text(json.dumps(todas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Total: {len(todas)} -> {args.salida}", file=sys.stderr)


if __name__ == "__main__":
    main()
