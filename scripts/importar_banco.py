"""
Importa los bancos de preguntas revisados (banco/*.json) a la tabla banco_preguntas de la app.

Cada pregunta se asocia a su unidad del temario (documento + artículo), que la app crea al
sincronizar las carpetas de PDFs. Las preguntas ya importadas (mismo enunciado en la misma
unidad) se saltan, así que se puede ejecutar varias veces.

Uso:
    python scripts/importar_banco.py banco/*.json
    python scripts/importar_banco.py banco/*.json --db /ruta/adif_2026_estado.db
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
import motor_adaptativo as motor  # noqa: E402


def buscar_unidad(cur, documento: str, articulo: str) -> int | None:
    cur.execute(
        "SELECT id FROM unidades_temario WHERE documento = ? AND codigo_unidad = ? ORDER BY id LIMIT 1",
        (documento, articulo),
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    # «Artículo 1» no debe caer en «Artículo 10»: solo se acepta el respaldo por prefijo exacto + punto o espacio
    cur.execute(
        "SELECT id, codigo_unidad FROM unidades_temario WHERE documento = ? AND codigo_unidad LIKE ? ORDER BY id",
        (documento, f"{articulo}%"),
    )
    for r in cur.fetchall():
        resto = r["codigo_unidad"][len(articulo):]
        if not resto or not resto[0].isdigit():
            return r["id"]
    return None


def importar(ruta: Path) -> tuple[int, int, list[str]]:
    banco = json.loads(ruta.read_text(encoding="utf-8"))
    documento = unicodedata.normalize("NFC", banco["documento"])
    conn = motor.get_db_connection()
    cur = conn.cursor()
    nuevas, repetidas, sin_unidad = 0, 0, []

    for p in banco["preguntas"]:
        unidad_id = buscar_unidad(cur, documento, p["articulo"])
        if unidad_id is None:
            sin_unidad.append(f"{p['id']} ({p['articulo']})")
            continue
        cur.execute(
            "SELECT 1 FROM banco_preguntas WHERE unidad_id = ? AND enunciado = ?",
            (unidad_id, p["enunciado"]),
        )
        if cur.fetchone():
            repetidas += 1
            continue
        cur.execute(
            """
            INSERT INTO banco_preguntas (
                unidad_id, nivel, es_refuerzo, trampa_objetivo, enunciado,
                opciones_json, indice_correcta, cita_literal_boe,
                explicacion_detallada, trampas_por_opcion_json, usada
            ) VALUES (?, ?, 0, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                unidad_id,
                p["nivel"],
                p.get("trampa_objetivo", ""),
                p["enunciado"],
                json.dumps(p["opciones"], ensure_ascii=False),
                p["indice_correcta"],
                p["cita_literal_boe"],
                p["explicacion_detallada"],
                json.dumps(p["trampas_por_opcion"], ensure_ascii=False),
            ),
        )
        nuevas += 1

    conn.commit()
    conn.close()
    return nuevas, repetidas, sin_unidad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bancos", nargs="+", type=Path)
    ap.add_argument("--db", type=Path, help="Base de datos de la app (por defecto, la de app/)")
    args = ap.parse_args()

    if args.db:
        motor.DB_PATH = args.db
    if not Path(motor.DB_PATH).exists():
        sys.exit(f"No existe {motor.DB_PATH}. Arranca antes la app para que sincronice el temario.")

    for ruta in args.bancos:
        nuevas, repetidas, sin_unidad = importar(ruta)
        print(f"{ruta.name}: {nuevas} importadas, {repetidas} ya existían, {len(sin_unidad)} sin unidad")
        for s in sin_unidad:
            print(f"  ✗ sin unidad en el temario: {s}")


if __name__ == "__main__":
    main()
