"""
Extrae las preguntas (inglés y conocimientos) de los cuadernillos oficiales de ADIF, las cruza
con sus plantillas correctoras y une las versiones del mismo examen (mismas preguntas en otro orden).
Es la base de notebooklm/datos/preguntas_oficiales_2023_2025.json.

Uso:
    python3 scripts/radiografia_extraer.py tecnico_2023.pdf:"PNI23/03 Técnico 2023" \
        tecnico_av_2023.pdf:"PNI23/04 Técnico AV 2023" \
        cuadro_2025.pdf:"PNI25/02 Cuadro Técnico 2025" -o preguntas.json

Los cuadernillos van a dos columnas: cada página se recorta en dos mitades antes de extraer.
Algunas fuentes del PDF de 2025 salen como (cid:N); se traducen con chr(N + 29).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pdfplumber

RE_CODIGO = re.compile(r"C[óo]digo (?:de ex[áa]men|del libro):?\s*(\d{4})")
RE_PREGUNTA = re.compile(r"^(\d{1,3})\.\s*(.*)$")
RE_OPCION = re.compile(r"^([a-dA-D])\)\s*(.*)$")
RE_SECCION = re.compile(r"^\s*(Reserva\s+)?(Ingl[ée]s|Conocim\w*(?:\s+(?:General|Espec[íi]fico))?)\s*$", re.I)
RUIDO = re.compile(r"^(P[áa]gina \d+|NO ABRA.*|Test Psicom.*|Todos los derechos.*)$")

# Plantillas publicadas como página girada (pdfplumber no siempre las lee). PNI25/02, Área Gestión.
PLANTILLAS_MANUALES = {"3214": "BCDADCCCADBCCBABAD", "4004": "CCCBDCADABCADCBDCC"}

# Versiones en las que el recorte a dos columnas mezcla líneas de dos opciones: se usa la otra versión.
PREFERIR = {"3311#47"}

# Qué prueba es cada código de examen y qué números son de reserva.
PRUEBAS = {
    ("3233", "3311", "1020", "1322"): (lambda n: "Inglés" if n <= 36 else "Conocimientos (temario común Técnico)",
                                       lambda n: n in (34, 35, 36) or n >= 67),
    ("1213", "4240"): (lambda n: "Inglés" if n <= 36 else "Conocimiento General",
                       lambda n: n in (34, 35, 36) or n >= 52),
    ("2130", "4131"): (lambda n: "Conocimiento Específico (resto perfiles técnicos)", lambda n: n >= 16),
    ("3214", "4004"): (lambda n: "Conocimiento Específico (Área Gestión)", lambda n: n >= 16),
}


def cid(s: str) -> str:
    return re.sub(r"\(cid:(\d+)\)", lambda m: chr(int(m.group(1)) + 29), s)


def limpia(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+Reserva\b.*$", "", s)
    s = re.sub(r"\s+(?:Espec)?í?fico$", "", s).strip()
    return s.replace("elsector", "el sector")


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", unicodedata.normalize("NFKD", s.lower())).strip()


def leer_plantillas(pdf) -> dict[str, dict[int, str]]:
    res: dict[str, dict[int, str]] = {c: {i + 1: l for i, l in enumerate(v)} for c, v in PLANTILLAS_MANUALES.items()}
    for page in pdf.pages[:8]:
        texto = page.extract_text() or ""
        if "Respuesta correcta" not in texto:
            continue
        codigos: list[str] = []
        for linea in texto.splitlines():
            encontrados = RE_CODIGO.findall(linea)
            if encontrados:
                codigos = encontrados
                for c in codigos:
                    res.setdefault(c, {})
                continue
            pares = re.findall(r"(\d{1,2})\s+([A-D]|RESERVA)\b", linea)
            if codigos and len(pares) == len(codigos):
                for c, (n, letra) in zip(codigos, pares):
                    if letra != "RESERVA":
                        res[c].setdefault(int(n), letra)
    return res


def columnas(page) -> list[str]:
    mitad = page.width / 2
    izq = page.crop((0, 0, mitad, page.height)).extract_text() or ""
    der = page.crop((mitad, 0, page.width, page.height)).extract_text() or ""
    return izq.splitlines() + der.splitlines()


def parsear(lineas: list[str]) -> list[dict]:
    preguntas: list[dict] = []
    actual: dict | None = None
    for bruta in lineas:
        s = cid(bruta).strip()
        if not s or RUIDO.match(s) or RE_SECCION.match(s):
            continue
        m_p, m_o = RE_PREGUNTA.match(s), RE_OPCION.match(s)
        if m_p and (actual is None or len(actual["opciones"]) == 4):
            actual = {"numero": int(m_p.group(1)), "enunciado": m_p.group(2), "opciones": []}
            preguntas.append(actual)
            continue
        if actual is None:
            continue
        n_op = len(actual["opciones"])
        if m_o and n_op < 4 and m_o.group(1).lower() == "abcd"[n_op]:
            actual["opciones"].append(m_o.group(2))
        elif actual["opciones"]:
            actual["opciones"][-1] += " " + s
        else:
            actual["enunciado"] += " " + s
    return [p for p in preguntas if len(p["opciones"]) == 4]


def extraer(ruta: Path, convocatoria: str) -> list[dict]:
    salida: list[dict] = []
    with pdfplumber.open(ruta) as pdf:
        plantillas = leer_plantillas(pdf)
        libros: dict[str, list[str]] = {}
        codigo = None
        for page in pdf.pages:
            texto = cid(page.extract_text() or "")
            m = RE_CODIGO.search(texto)
            if m and "INSTRUCCIONES" in texto:
                codigo = m.group(1)
                libros[codigo] = []
                continue
            if codigo and "Respuesta correcta" not in texto:
                libros[codigo].extend(columnas(page))
        for codigo, lineas in libros.items():
            prueba_de, es_reserva = next(v for k, v in PRUEBAS.items() if codigo in k)
            for p in parsear(lineas):
                n = p["numero"]
                salida.append({
                    "convocatoria": convocatoria, "codigo_examen": codigo, "numero": n,
                    "prueba": prueba_de(n), "reserva": es_reserva(n),
                    "enunciado": limpia(p["enunciado"]), "opciones": [limpia(o) for o in p["opciones"]],
                    "correcta": plantillas.get(codigo, {}).get(n),
                })
    return salida


def unir_versiones(preguntas: list[dict]) -> list[dict]:
    """Las versiones de un mismo examen traen las mismas preguntas en otro orden: se dejan una vez."""
    unicas: dict[tuple, dict] = {}
    for q in preguntas:
        texto_ok = q["opciones"]["ABCD".index(q["correcta"])] if q["correcta"] else ""
        clave = (q["convocatoria"], norm(q["enunciado"]), norm(texto_ok) or norm(" ".join(sorted(q["opciones"]))))
        version = f'{q["codigo_examen"]}#{q["numero"]}'
        if clave not in unicas:
            unicas[clave] = {**q, "versiones": [version], "correcta_texto": texto_ok or None}
            continue
        u = unicas[clave]
        u["versiones"].append(version)
        if version in PREFERIR or (not u["correcta"] and q["correcta"]):
            u.update(opciones=q["opciones"], correcta=q["correcta"], codigo_examen=q["codigo_examen"],
                     numero=q["numero"], correcta_texto=texto_ok or u["correcta_texto"])
    resultado = list(unicas.values())
    for i, q in enumerate(resultado, 1):
        q["id"] = i
    return resultado


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("entradas", nargs="+", help='ruta.pdf:"convocatoria"')
    ap.add_argument("-o", "--salida", required=True)
    args = ap.parse_args()
    todas: list[dict] = []
    for entrada in args.entradas:
        ruta, _, conv = entrada.partition(":")
        todas.extend(extraer(Path(ruta), conv))
    unicas = unir_versiones(todas)
    Path(args.salida).write_text(json.dumps(unicas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(todas)} preguntas leídas -> {len(unicas)} únicas -> {args.salida}", file=sys.stderr)


if __name__ == "__main__":
    main()
