# salidas/

Aquí va TODO lo que se genere (simulacros HTML, exámenes, informes). Un solo sitio.

| Fichero | Qué es |
|---|---|
| `simulacro_gestion_01.html` | Test completo de Gestión 01 (LGSS), 30 preguntas |
| `examen_mixto.html` | 18 preguntas sorteadas de Gestión 01 y 02 (15 + 3 reserva) |

Los bancos de preguntas siguen en `banco/`. Los extractos de trabajo (`tmp/`) no se versionan.

Regenerar:
    python3 scripts/generar_simulacro.py banco/*.json --aleatorio 18 -o salidas/examen_<fecha>.html
