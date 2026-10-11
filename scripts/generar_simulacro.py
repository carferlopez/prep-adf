"""
Genera la página de simulacro (HTML autocontenido) a partir de uno o varios bancos.

Uso:
    python scripts/generar_simulacro.py banco/gestion_02_ley_47_2003.json -o tmp/simulacro.html
    python scripts/generar_simulacro.py banco/*.json -o tmp/multi.html                   # varias normas a la vez
    python scripts/generar_simulacro.py banco/*.json --aleatorio 18 -o tmp/examen.html   # 15 + 3 de reserva
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def nombre_corto(norma: str) -> str:
    """«Ley 47/2003, de 26 de noviembre, General Presupuestaria» -> «Ley 47/2003»."""
    return norma.split(",")[0].strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bancos", nargs="+", type=Path)
    ap.add_argument("-o", "--salida", type=Path, required=True)
    ap.add_argument("--aleatorio", type=int, help="Número de preguntas a sortear entre todos los bancos")
    ap.add_argument("--titulo", help="Título de la página")
    args = ap.parse_args()

    bancos = [json.loads(b.read_text(encoding="utf-8")) for b in args.bancos]
    multi = len(bancos) > 1

    normas, preguntas, vistos = [], [], set()
    for k, (ruta, b) in enumerate(zip(args.bancos, bancos)):
        larga = b.get("norma") or ruta.stem
        normas.append({"clave": ruta.stem, "corta": nombre_corto(larga), "larga": larga, "n": len(b["preguntas"])})
        for p in b["preguntas"]:
            pid = p["id"] if p["id"] not in vistos else f"{ruta.stem}:{p['id']}"  # ids únicos entre bancos
            vistos.add(pid)
            preguntas.append(p | {"id": pid, "norma": k})
    if args.aleatorio:
        preguntas = random.sample(preguntas, min(args.aleatorio, len(preguntas)))
        for k, n in enumerate(normas):
            n["n"] = sum(p["norma"] == k for p in preguntas)

    if not multi:
        h1 = f"Simulacro {bancos[0].get('norma', '')}"
        titulo = args.titulo or h1.split(",")[0]
        sub = bancos[0].get("bloque_temario", "").title()
    else:
        titulo = h1 = args.titulo or ("Examen aleatorio ADIF" if args.aleatorio else "Simulacro ADIF")
        sub = f"{sum(n['n'] > 0 for n in normas)} normas · preguntas verificadas contra el BOE"
    datos_banco = {"preguntas": preguntas, "normas": normas, "agrupar": multi and not args.aleatorio}

    html = (RAIZ / "simulacro" / "plantilla.html").read_text(encoding="utf-8")
    datos = json.dumps(datos_banco, ensure_ascii=False).replace("</", "<\\/")
    for marca, valor in {
        "__TITULO__": titulo, "__H1__": h1, "__SUB__": sub, "__N__": str(len(preguntas)),
        "__CLAVE__": "simulacro-" + "-".join(sorted(b.stem for b in args.bancos))[:80],
        "__BANCO__": datos,
    }.items():
        html = html.replace(marca, valor)

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(html, encoding="utf-8")
    desglose = ", ".join(f"{n['corta']}: {n['n']}" for n in normas)
    print(f"{args.salida}: {len(preguntas)} preguntas de {len(bancos)} banco(s) ({desglose})")


if __name__ == "__main__":
    main()
