# Encargo: banco de 30 preguntas de un tema (sesión corta)

Lee SOLO el extracto `tmp/<tema>.md`. No leas la ley entera, los exámenes ni `adn_tribunal.md`. Si falta el extracto, genéralo:
`python3 scripts/preparar_tema.py "<PDF>" -o tmp/<tema>.md` (descarga el PDF de Drive a un fichero; nunca muestres su contenido en el chat).

## Estilo del tribunal (resumen de 559 preguntas oficiales)
- 4 opciones, una correcta. La correcta reproduce casi literalmente el texto del extracto.
- Enunciado: 75 % `¿…?` y 25 % frase a completar terminada en `:`. Suele empezar por «Según la Ley X/AAAA, …» o «Según el artículo N de …».
- Unas 4 de 30 con formulación negativa: `NO` en mayúsculas o «Señale la afirmación INCORRECTA».
- Distractores verosímiles sacados de la misma norma: cifra desplazada (serie 2/3/4/6), órgano cambiado (otro órgano que sí aparece en la ley), regla y excepción invertidas, elemento ajeno en una enumeración, ámbito ampliado o reducido. Como mucho uno «de sentido común».
- Nunca «todas/ninguna de las anteriores». Opciones con la misma estructura gramatical y longitudes parecidas.
- No preguntar por fechas de publicación, derogaciones ni números de disposición.
- Niveles: unas 12 de nivel 1 (dato principal), 12 de nivel 2 (trampa fina) y 6 de nivel 3 (excepción o supuesto).
- Correctas repartidas entre A, B, C y D (7-8 de cada). Como mucho 2 preguntas por artículo.

## Formato: `banco/<tema>.json`
```json
{"documento": "<nombre EXACTO del PDF>", "bloque_temario": "<carpeta del temario>", "norma": "<título>",
 "preguntas": [{"id": "XXX-001", "articulo": "Artículo N", "nivel": 1, "trampa_objetivo": "≤10 palabras",
   "enunciado": "…", "opciones": ["…","…","…","…"], "indice_correcta": 0,
   "cita_literal_boe": "copia EXACTA del extracto; varios fragmentos separados por […]",
   "explicacion_detallada": "2 frases como máximo",
   "trampas_por_opcion": ["una línea", "…", "…", "…"]}]}
```
- `articulo` es igual al encabezado `## Artículo N` del extracto (lo usa el importador).
- En las explicaciones, nunca nombres letras de opción («la B»): la app baraja.

## Cierre
1. `python3 scripts/validar_banco.py banco/<tema>.json --pdf "<PDF>"` → corrige solo lo que falle hasta 0 errores.
2. Commit + push a la rama de trabajo. En el chat, responde solo con una línea: el tema, n.º de preguntas y «0 errores».
