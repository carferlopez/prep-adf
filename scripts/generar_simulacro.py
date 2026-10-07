"""
Genera la página de simulacro (HTML autocontenido) a partir de uno o varios bancos.

Uso:
    python scripts/generar_simulacro.py banco/gestion_02_ley_47_2003.json -o tmp/simulacro.html
    python scripts/generar_simulacro.py banco/*.json --aleatorio 18 -o tmp/examen.html   # 15 + 3 de reserva
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bancos", nargs="+", type=Path)
    ap.add_argument("-o", "--salida", type=Path, required=True)
    ap.add_argument("--aleatorio", type=int, help="Número de preguntas a sortear entre todos los bancos")
    ap.add_argument("--titulo", help="Título de la página")
    args = ap.parse_args()

    bancos = [json.loads(b.read_text(encoding="utf-8")) for b in args.bancos]
    preguntas = [p | {"articulo": f"{b.get('norma', '')} · {p['articulo']}" if len(bancos) > 1 else p["articulo"]}
                 for b in bancos for p in b["preguntas"]]
    if args.aleatorio:
        preguntas = random.sample(preguntas, min(args.aleatorio, len(preguntas)))

    if len(bancos) == 1:
        h1 = f"Simulacro {bancos[0].get('norma', '')}"
        titulo = args.titulo or h1.split(",")[0]
        sub = bancos[0].get("bloque_temario", "").title()
    else:
        titulo = h1 = args.titulo or ("Examen aleatorio ADIF" if args.aleatorio else "Simulacro ADIF")
        sub = f"{len(bancos)} temas · preguntas verificadas contra el BOE"

    html = (RAIZ / "simulacro" / "plantilla.html").read_text(encoding="utf-8")
    datos = json.dumps({"preguntas": preguntas}, ensure_ascii=False).replace("</", "<\\/")
    for marca, valor in {
        "__TITULO__": titulo, "__H1__": h1, "__SUB__": sub, "__N__": str(len(preguntas)),
        "__CLAVE__": "simulacro-" + "-".join(sorted(b.stem for b in args.bancos))[:80],
        "__BANCO__": datos,
    }.items():
        html = html.replace(marca, valor)

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(html, encoding="utf-8")
    print(f"{args.salida}: {len(preguntas)} preguntas de {len(bancos)} banco(s)")


if __name__ == "__main__":
    main()
