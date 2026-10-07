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
