"""
Prepara el extracto de alto rendimiento de un tema para redactar su banco sin leer la ley entera.

Trocea el PDF por artículos (misma lógica que la app), puntúa cada artículo por:
  - menciones en preguntas oficiales de la misma norma (estilo/ejemplos.json),
  - densidad de datos «examinables»: cifras, plazos, porcentajes y órganos competentes,
y escribe tmp/<salida>.md con los mejores artículos hasta ~24.000 caracteres, en orden legal.

Uso:
    python scripts/preparar_tema.py "ruta/02 Ley 47_2003....pdf" -o tmp/gestion_02.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "app"))
import motor_adaptativo as motor  # noqa: E402

RE_DATO = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:%|por ciento|euros|días|meses|años|horas)|\b(?:un|dos|tres|cuatro|cinco|seis|siete|diez|quince|veinte|treinta)\s+(?:días|meses|años|por ciento)",
    re.IGNORECASE,
)
RE_ORGANO = re.compile(
    r"Consejo de Ministros|Gobierno|Ministr[oa]|Tribunal|Intervención|Dirección General|Consejo de Administración|Presidente|Director|Cortes Generales|Comisión",
)


def numero_articulo(codigo: str) -> int | None:
    m = re.search(r"(\d+)", codigo)
    return int(m.group(1)) if m else None


def menciones_oficiales(clave: str | None) -> tuple[dict[int, int], int]:
    """Artículos citados en preguntas oficiales de esta norma y total de preguntas de la norma."""
    if not clave:
        return {}, 0
    exacta = re.compile(rf"(?<!\d){re.escape(clave)}")
    citas: dict[int, int] = {}
    total = 0
    for p in json.loads((RAIZ / "estilo" / "ejemplos.json").read_text(encoding="utf-8")):
        if not exacta.search(p["enunciado"]):
            continue
        total += 1
        for n in re.findall(r"art[íi]culo\s+(\d+)", p["enunciado"], re.IGNORECASE):
            citas[int(n)] = citas.get(int(n), 0) + 1
    return citas, total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("-o", "--salida", type=Path, required=True)
    ap.add_argument("--max-chars", type=int, default=24000)
    ap.add_argument("--max-por-articulo", type=int, default=1000)
    ap.add_argument("--norma", help="Clave de la norma (p. ej. 47/2003) si no se deduce del nombre del PDF")
    args = ap.parse_args()

    nombre = unicodedata.normalize("NFC", args.pdf.name)
    unidades = motor.trocear_documento_adif("", nombre, motor.extraer_texto_pdf_o_txt(args.pdf))
    clave = args.norma or motor._clave_norma(nombre)
    citas, total_oficiales = menciones_oficiales(clave)

    puntuadas = []
    for i, u in enumerate(unidades):
        texto = u["contenido_literal"]
        n = numero_articulo(u["codigo_unidad"])
        puntos = 30 * citas.get(n, 0) + 2 * len(RE_DATO.findall(texto)) + len(RE_ORGANO.findall(texto))
        puntos /= max(1.0, len(texto) / 1500) ** 0.5  # no premiar solo por longitud
        if i < 3:
            puntos += 15  # objeto, ámbito y definiciones: el tribunal los pregunta casi siempre
        puntuadas.append((puntos, u))

    elegidas, usados = [], 0
    for puntos, u in sorted(puntuadas, key=lambda x: -x[0]):
        texto = u["contenido_literal"][: args.max_por_articulo]
        if usados + len(texto) > args.max_chars:
            continue
        elegidas.append(u | {"contenido_literal": texto})
        usados += len(texto)

    elegidas.sort(key=lambda u: (numero_articulo(u["codigo_unidad"]) or 0, u["codigo_unidad"]))
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    with args.salida.open("w", encoding="utf-8") as f:
        f.write(f"# Extracto: {nombre}\n\n")
        f.write(f"Norma {clave or 's/n'} · {len(unidades)} unidades · {len(elegidas)} seleccionadas · "
                f"{total_oficiales} preguntas oficiales de esta norma · artículos preguntados: "
                f"{', '.join(str(k) for k in sorted(citas)) or 'ninguno citado'}\n\n")
        for u in elegidas:
            f.write(f"## {u['codigo_unidad']}\n\n{u['contenido_literal'].strip()}\n\n")
    print(f"{args.salida}: {len(elegidas)}/{len(unidades)} unidades, {usados} caracteres")


if __name__ == "__main__":
    main()
