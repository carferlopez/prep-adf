# prep-adf

Preparación de la OEP 2026 de ADIF (Técnico: Gestión y Comunicación). Incluye el entrenador adaptativo, un banco de preguntas revisadas al estilo del Tribunal y las herramientas para comprobar que cada pregunta se apoya en el texto literal del BOE.

## Estructura

| Ruta | Qué es |
|---|---|
| `app/` | Entrenador adaptativo: `servidor.py` (web local en el puerto 8826), `motor_adaptativo.py` (SQLite + Gemini) y `coach_feynman.py`. |
| `estilo/adn_tribunal.md` | Guía de estilo del Tribunal, sacada de 559 preguntas oficiales de 2022 a 2025. |
| `estilo/ejemplos.json` | Corpus de esas preguntas oficiales, con la respuesta de la plantilla correctora cuando existe. |
| `banco/*.json` | Preguntas redactadas y revisadas por tema, cada una con su cita literal del BOE. |
| `scripts/` | Extracción de exámenes, validación del banco e importación en la app. |
| `notebooklm/` | Radiografía del Tribunal (Técnico 2023, Técnico AV 2023 y Cuadro Técnico 2025), las 180 preguntas oficiales anotadas y el prompt maestro para estudiar en NotebookLM (Gemini Notebook). |

## Uso

La app espera la estructura de carpetas de Drive (`TEMARIO …/`, `EXÁMENES AÑOS ANTERIORES/`) junto a los `.py`, igual que en `ADIF 2026/APP`. La carpeta `static/` y los PDFs no se versionan.

```bash
# 1. Arrancar la app (sincroniza los PDFs del temario y carga los ejemplos oficiales)
cd "ADIF 2026/APP" && python3 servidor.py

# 2. Validar un banco contra su PDF oficial: todas las citas deben aparecer literalmente
python3 scripts/validar_banco.py banco/*.json --temario "ADIF 2026/APP"

# 3. Importar el banco en la base de datos de la app (se puede repetir sin duplicar)
python3 scripts/importar_banco.py banco/*.json --db "ADIF 2026/APP/adif_2026_estado.db"

# Regenerar el corpus de estilo a partir de los cuadernillos oficiales
python3 scripts/extraer_examenes.py ex2025.pdf:2025 ex2024.pdf:2024 … -o estilo/ejemplos.json
```

Para que la app encuentre la guía y los ejemplos, copia `estilo/` dentro de `ADIF 2026/APP/` (o deja la app dentro de este repositorio).

## Generador de preguntas con Gemini

`generar_pregunta_con_gemini` ahora:

- incluye en el prompt la guía de `estilo/adn_tribunal.md`;
- usa como ejemplos preguntas **oficiales de la misma norma** (por ejemplo, las de la Ley 47/2003 cuando pregunta sobre la LGP), con su respuesta de plantilla;
- descarta las preguntas cuya cita no aparece literalmente en el artículo, las que revelan la respuesta en el enunciado o las que tienen la correcta desproporcionadamente larga, y en ese caso prueba con el siguiente modelo.

## Estado del banco

| Tema | Preguntas | Citas verificadas |
|---|---|---|
| Gestión 02 · Ley 47/2003 General Presupuestaria | 30 | 30/30 |

## Radiografía del Tribunal para NotebookLM

`notebooklm/` contiene el material para usar NotebookLM (desde julio de 2026, Gemini Notebook) como generador de tests al estilo del Tribunal. Las instrucciones de uso, en 3 pasos, están en `notebooklm/README.md`.

| Fichero | Para qué |
|---|---|
| `PROMPT_MAESTRO.md` | Los textos que hay que copiar. El prompt 1 es para el informe interactivo del Studio, uno por norma, cambiando solo la línea `NORMA:`. Los prompts 2 y 3 son los informes interactivos de inglés y de psicotécnico, cambiando solo la línea `FOCO:`. El prompt 4, opcional, va una vez en las instrucciones del chat de cada cuaderno, para simulacros y corrección de fallos. |
| `01_radiografia_tribunal.md` | Cómo pregunta el Tribunal: cifras, algoritmo, plantillas de enunciado, recetas de distractores, mapa de contenidos, trampas, inglés y estrategia. Se sube como fuente. |
| `02_preguntas_oficiales_anotadas.md` | Las 180 preguntas oficiales (126 de conocimientos y 54 de inglés) con su clave y su anotación. Se sube como fuente. |

Para regenerarlo con otros cuadernillos:

```bash
python3 scripts/radiografia_extraer.py t2023.pdf:"PNI23/03 Técnico 2023" av2023.pdf:"PNI23/04 Técnico AV 2023" c2025.pdf:"PNI25/02 Cuadro Técnico 2025" -o preguntas.json
python3 scripts/radiografia_estadisticas.py notebooklm/datos/preguntas_oficiales_2023_2025.json > notebooklm/datos/estadisticas_objetivas.txt
python3 scripts/radiografia_corpus_anotado.py notebooklm/datos/preguntas_oficiales_2023_2025.json -o notebooklm/02_preguntas_oficiales_anotadas.md
```

Las anotaciones de cada pregunta (norma, artículo, tipo de dato, distractores y trampa) se hicieron con un análisis asistido por IA, con una revisión dirigida de los casos dudosos. Hay que contrastar el artículo con el BOE consolidado antes de memorizarlo.
