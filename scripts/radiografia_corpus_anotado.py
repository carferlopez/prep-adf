"""
Genera notebooklm/02_preguntas_oficiales_anotadas.md (fuente «Preguntas oficiales anotadas» de NotebookLM)
a partir de notebooklm/datos/preguntas_oficiales_2023_2025.json.

Uso:
    python3 scripts/radiografia_corpus_anotado.py \
        notebooklm/datos/preguntas_oficiales_2023_2025.json -o notebooklm/02_preguntas_oficiales_anotadas.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

OPERACION = {
    "quien_organo_competente": "Órgano competente («quién»)",
    "cifra_porcentaje_cuantia": "Cifra o cuantía",
    "plazo_tiempo": "Plazo o tiempo",
    "definicion_concepto": "Definición (se da el término)",
    "denominacion_nombre_figura": "Denominación (se da la definición)",
    "enumeracion_cual_si_pertenece": "Lista: cuál sí pertenece",
    "enumeracion_intruso_no_pertenece": "Lista: intruso («cuál NO»)",
    "clasificacion_tipos": "Clasificación",
    "regla_general_vs_excepcion": "Regla general frente a excepción",
    "ambito_aplicacion_sujetos": "Ámbito o sujetos",
    "requisito_condicion": "Requisito o condición",
    "procedimiento_tramite": "Procedimiento o trámite",
    "efecto_consecuencia_juridica": "Efecto jurídico",
    "derecho_obligacion_prohibicion": "Derecho, obligación o prohibición",
    "afirmaciones_vf_mixtas": "Afirmaciones mixtas",
    "dato_corporativo_adif_red": "Dato corporativo de Adif",
    "otro": "Otro",
}
ARQUETIPO = {
    "cifra_desplazada": "Cifra desplazada",
    "unidad_o_plazo_cambiado": "Unidad o plazo cambiado",
    "organo_o_sujeto_cambiado": "Órgano o sujeto cambiado",
    "regla_excepcion_invertida": "Regla y excepción invertidas",
    "absoluto_anadido": "Absoluto añadido",
    "condicion_anadida_o_suprimida": "Condición añadida o suprimida",
    "ambito_ampliado_o_reducido": "Ámbito ampliado o reducido",
    "elemento_de_otra_lista": "Elemento de otra lista",
    "termino_parecido_confundible": "Término parecido confundible",
    "verbo_modal_cambiado": "Verbo modal cambiado",
    "negacion_o_inversion_de_la_correcta": "Negación o inversión de la correcta",
    "mezcla_de_conceptos": "Mezcla de conceptos",
    "plausible_inventado": "Plausible inventado",
    "sentido_comun_absurdo": "Sentido común absurdo",
    "afirmacion_verdadera_literal": "Afirmación verdadera literal",
    "otro": "Otro",
}
FORMA = {
    "pregunta_directa": "pregunta directa",
    "frase_a_completar": "frase a completar",
    "elegir_afirmacion_correcta": "elegir la afirmación correcta",
    "elegir_afirmacion_incorrecta": "elegir la afirmación incorrecta",
    "supuesto_practico": "supuesto práctico",
}
TIPO_EN = {
    "vocabulario_campo_semantico": "Vocabulario y campo semántico",
    "phrasal_verb": "Phrasal verb",
    "colocacion_preposicion": "Colocación o preposición",
    "gramatica": "Gramática",
    "reformulacion_equivalente": "Reformulación equivalente",
    "idiom_proverbio": "Idiom o proverbio",
    "funcion_comunicativa_respuesta": "Función comunicativa",
    "registro_informal": "Registro informal",
    "comprension_aviso_texto": "Aviso, cartel o titular",
    "otro": "Otro (formación de palabras)",
}

CABECERA = """# Preguntas oficiales anotadas · Adif 2023-2025

Fuente de ejemplos reales para NotebookLM. Acompaña a «Radiografía del Tribunal» (`01_radiografia_tribunal.md`), que cita estas preguntas por su **Q-id**.

- **Origen:** cuadernillos y plantillas correctoras oficiales de Adif: Técnico PNI23/03 (4-11-2023), Técnico Adif Alta Velocidad PNI23/04 (4-11-2023) y Mando Intermedio y Cuadro PNI25/02 (15-11-2025). Las versiones del mismo examen (mismas preguntas en otro orden) aparecen una sola vez; en «versiones» figura el código de examen y el número en cada una.
- **Clave:** «← CORRECTA» marca la respuesta de la plantilla oficial. Las reservas de 2023 no se usaron y no tienen clave: se indica una **respuesta razonada (no oficial)**.
- **Anotación:** norma y artículo probable (con su grado de confianza), tipo de dato preguntado, forma, plantilla del enunciado, tipo de cada distractor, trampa, cómo resolverla y qué memorizar. La hizo un análisis asistido por IA y una revisión dirigida de los casos dudosos: **comprueba el artículo en el BOE consolidado antes de memorizarlo** y ten en cuenta que alguna norma ha cambiado desde el examen.
- **Uso:** son moldes de estilo. No se copian como preguntas nuevas y no son materia de examen en sí mismas.

| Bloque | Q-id |
|---|---|
| Técnico 2023 · Inglés | Q1–Q18 |
| Técnico 2023 · Conocimientos (temario común) | Q19–Q54 |
| Técnico AV 2023 · Inglés | Q55–Q72 |
| Técnico AV 2023 · Conocimientos (temario común) | Q73–Q108 |
| Cuadro Técnico 2025 · Inglés | Q109–Q126 |
| Cuadro Técnico 2025 · Conocimiento General | Q127–Q144 |
| Cuadro Técnico 2025 · Específico perfiles técnicos | Q145–Q162 |
| Cuadro Técnico 2025 · Específico Área de Gestión | Q163–Q180 |
"""


def bloque_conocimientos(q: dict) -> list[str]:
    a = q["anotacion"]
    lineas = [
        f'- **Norma:** {a["norma"]} · **Artículo probable:** {a["articulo_probable"]} (confianza {a["confianza_articulo"]}) · **Bloque:** {a["bloque"]}',
        f'- **Dato preguntado:** {OPERACION.get(a["operacion"], a["operacion"])} · **Forma:** {FORMA.get(a["forma"], a["forma"])}, {a["polaridad"]} · **Nivel:** {a["dificultad"]} · **Correcta:** {a["correcta_literalidad"].replace("_", " ")}',
        f'- **Plantilla:** {a["plantilla"]}',
        "- **Opciones que no son la respuesta:**",
    ]
    lineas += [f'  - {d["letra"].lower()}) *{ARQUETIPO.get(d["arquetipo"], d["arquetipo"])}*: {d["explicacion"]}' for d in a["distractores"]]
    lineas += [
        f'- **Trampa:** {a["trampa_principal"]}',
        f'- **Cómo resolverla:** {a["pista_resolucion"]}',
        f'- **Qué memorizar:** {a["que_hay_que_memorizar"]}',
    ]
    if a["coherencia_respuesta_oficial"] in ("dudosa", "incorrecta"):
        lineas.append(f'- **⚠ Clave {a["coherencia_respuesta_oficial"]}:** {a["nota_calidad"]}')
    elif a["coherencia_respuesta_oficial"] == "sin_respuesta":
        lineas.append(f'- **Respuesta razonada (no oficial):** {a["respuesta_propuesta"].lower()}). {a["nota_calidad"]}')
    return lineas


def bloque_ingles(q: dict) -> list[str]:
    a = q["anotacion"]
    lineas = [
        f'- **Tipo:** {TIPO_EN.get(a["tipo"], a["tipo"])} · **Punto evaluado:** {a["punto_concreto"]} · **Nivel MCER:** {a["nivel_mcer"]}',
        f'- **Distractores:** {a["patron_distractores"]}',
        f'- **Trampa:** {a["trampa"]}',
    ]
    if a["coherencia_respuesta_oficial"] == "sin_respuesta":
        lineas.append(f'- **Respuesta razonada (no oficial):** {a["respuesta_propuesta"].lower()})')
    elif a["coherencia_respuesta_oficial"] != "coherente":
        lineas.append(f'- **⚠ Clave {a["coherencia_respuesta_oficial"]}:** revisa la explicación de la trampa.')
    return lineas


def render(preguntas: list[dict]) -> str:
    partes = [CABECERA]
    seccion = None
    for q in preguntas:
        cab = f'{q["convocatoria"]} — {q["prueba"]}'
        if cab != seccion:
            partes.append(f"\n## {cab}\n")
            seccion = cab
        reserva = " · RESERVA" if q["reserva"] else ""
        lineas = [f'### Q{q["id"]}{reserva} · versiones {", ".join(q["versiones"])}', "", q["enunciado"], ""]
        for letra, opcion in zip("ABCD", q["opciones"]):
            marca = "  ← CORRECTA" if q["correcta"] == letra else ""
            lineas.append(f"{letra.lower()}) {opcion}{marca}  ")
        if not q["correcta"]:
            lineas.append("*(Sin clave oficial: reserva no utilizada.)*")
        lineas.append("")
        lineas += bloque_ingles(q) if q["prueba"] == "Inglés" else bloque_conocimientos(q)
        partes.append("\n".join(lineas) + "\n")
    return "\n".join(partes)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("datos")
    ap.add_argument("-o", "--salida", required=True)
    args = ap.parse_args()
    preguntas = json.loads(Path(args.datos).read_text(encoding="utf-8"))
    Path(args.salida).write_text(render(preguntas), encoding="utf-8")
    print(f"{len(preguntas)} preguntas -> {args.salida}")


if __name__ == "__main__":
    main()
