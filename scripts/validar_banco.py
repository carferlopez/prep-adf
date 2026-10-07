"""
Valida los bancos de preguntas de banco/*.json.

Comprueba:
  - Esquema: 4 opciones, índice correcto en rango, 4 análisis de trampas, campos obligatorios.
  - Que cada fragmento de `cita_literal_boe` (separados por «[…]») aparece literalmente en el
    texto del PDF oficial, normalizando espacios y saltos de línea.
  - Que no hay enunciados duplicados ni opciones repetidas dentro de una pregunta.
  - Estilo: las explicaciones no mencionan letras de opción (la app las baraja).

Uso:
    python scripts/validar_banco.py banco/gestion_02_ley_47_2003.json --pdf ruta/al/temario.pdf
    python scripts/validar_banco.py banco/*.json --temario "/ruta/ADIF 2026/APP"

Con --temario se busca el PDF por el nombre guardado en el campo `documento` del banco.
Sin PDF, solo se valida el esquema y el estilo.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

CAMPOS = ("id", "articulo", "nivel", "enunciado", "opciones", "indice_correcta",
          "cita_literal_boe", "explicacion_detallada", "trampas_por_opcion")
# «la opción B», «respuesta C» o «A)» suelto; no confunde referencias como «art. 63.1.a)»
RE_LETRA = re.compile(r"\b(?i:opci[óo]n|respuesta)\s+[A-D]\b|(?<![\w.])[A-D]\)")


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFC", texto)
    texto = texto.replace("­", "")
    texto = re.sub(r"[‘’‚‛]", "'", texto)
    texto = re.sub(r"[“”„]", '"', texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def texto_pdf(ruta: Path) -> str:
    salida = subprocess.check_output(["pdftotext", str(ruta), "-"], text=True)
    # Quitar cabeceras y pies del BOE consolidado, que cortan frases entre páginas
    lineas = [
        l for l in salida.splitlines()
        if not re.match(r"^\s*(BOLETÍN OFICIAL DEL ESTADO|LEGISLACIÓN CONSOLIDADA|Página \d+)\s*$", l)
    ]
    return normalizar("\n".join(lineas))


def validar(ruta_banco: Path, ruta_pdf: Path | None) -> list[str]:
    errores: list[str] = []
    banco = json.loads(ruta_banco.read_text(encoding="utf-8"))
    preguntas = banco["preguntas"]
    fuente = texto_pdf(ruta_pdf) if ruta_pdf else None

    vistos: set[str] = set()
    for p in preguntas:
        pid = p.get("id", "?")
        faltan = [c for c in CAMPOS if c not in p]
        if faltan:
            errores.append(f"{pid}: faltan campos {faltan}")
            continue
        if len(p["opciones"]) != 4:
            errores.append(f"{pid}: tiene {len(p['opciones'])} opciones")
        if len(set(map(normalizar, p["opciones"]))) != len(p["opciones"]):
            errores.append(f"{pid}: opciones repetidas")
        if not 0 <= p["indice_correcta"] < 4:
            errores.append(f"{pid}: indice_correcta fuera de rango")
        if len(p["trampas_por_opcion"]) != 4:
            errores.append(f"{pid}: trampas_por_opcion debe tener 4 elementos")
        if p["nivel"] not in (1, 2, 3):
            errores.append(f"{pid}: nivel debe ser 1, 2 o 3")

        clave = normalizar(p["enunciado"])
        if clave in vistos:
            errores.append(f"{pid}: enunciado duplicado")
        vistos.add(clave)

        for campo in ("explicacion_detallada", "trampas_por_opcion"):
            valor = p[campo] if isinstance(p[campo], str) else " ".join(p[campo])
            if RE_LETRA.search(valor):
                errores.append(f"{pid}: {campo} menciona letras de opción")

        if fuente is not None:
            for fragmento in re.split(r"\s*\[…\]\s*", p["cita_literal_boe"]):
                if fragmento and normalizar(fragmento) not in fuente:
                    errores.append(f"{pid}: cita no encontrada en el PDF: «{fragmento[:90]}…»")

    reparto = collections.Counter("ABCD"[p["indice_correcta"]] for p in preguntas if "indice_correcta" in p)
    negativas = sum(1 for p in preguntas if re.search(r"\bNO\b|INCORRECTA|\bSÍ\b", p.get("enunciado", "")))
    print(
        f"{ruta_banco.name}: {len(preguntas)} preguntas · correctas {dict(sorted(reparto.items()))} · "
        f"negativas/inversas {negativas} · {'citas verificadas' if fuente else 'sin PDF: citas NO verificadas'}",
        file=sys.stderr,
    )
    return errores


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bancos", nargs="+", type=Path)
    ap.add_argument("--pdf", type=Path, help="PDF oficial (si se valida un solo banco)")
    ap.add_argument("--temario", type=Path, help="Carpeta raíz donde buscar el PDF por nombre")
    args = ap.parse_args()

    total = 0
    for ruta in args.bancos:
        pdf = args.pdf
        if pdf is None and args.temario:
            nombre = json.loads(ruta.read_text(encoding="utf-8"))["documento"]
            candidatos = [c for c in args.temario.rglob("*.pdf")
                          if unicodedata.normalize("NFC", c.name) == unicodedata.normalize("NFC", nombre)]
            pdf = candidatos[0] if candidatos else None
        errores = validar(ruta, pdf)
        for e in errores:
            print(f"  ✗ {e}")
        total += len(errores)

    print(f"{total} errores")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
