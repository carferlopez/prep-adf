# Estudiar con NotebookLM en 4 pasos

NotebookLM se llama **Gemini Notebook** desde julio de 2026; es la misma herramienta y la misma web.

## 1. Crea tres cuadernos, uno por bloque del examen

| Cuaderno | Fuentes que subes |
|---|---|
| **Adif · General** | Ley 38/2015, Declaración sobre la Red vigente (y la del año siguiente si ya está publicada), Estatutos de Adif y ADIF-AV, LCSP, LPACAP, LRJSP, LOPDGDD, PRL, ENS, Reglamentos (UE) 402/2013 y 2018/762, LO 3/2007, Ley 4/2023, Ley 53/1984, TREBEP y lo que añadan las bases de 2026 |
| **Adif · Gestión** | LGSS, Estatuto de los Trabajadores, Ley 47/2003 y el resto del temario específico de Gestión |
| **Adif · Inglés** | Solo las dos guías |

En **los tres** subes también `01_radiografia_tribunal.md` y `02_preguntas_oficiales_anotadas.md`. No hace falta que las leas: le enseñan a NotebookLM cómo pregunta el tribunal.

Las normas, en PDF con texto del **BOE consolidado**. Si un `.md` no carga, cámbiale la extensión a `.txt`.

¿Por qué por bloques y no una norma por cuaderno? El examen se hace por bloques. Así NotebookLM te avisa de las confusiones entre normas (por ejemplo, días hábiles en la LPACAP y naturales en la LCSP) y puede hacerte simulacros reales. Aun así, **estudias una norma por sesión**.

## 2. Pega el prompt maestro una vez en cada cuaderno

Abre `PROMPT_MAESTRO.md` y copia el bloque de texto en Chat → icono de ajustes → «Configurar chat» → «Personalizado». Es el mismo texto para los tres cuadernos. La primera vez, comprueba que sigue ahí al volver a abrir el cuaderno.

## 3. Estudia escribiendo en el chat

- `Norma: Ley 39/2015`: te da la radiografía de la norma, una ficha esencial, un test de 10 preguntas y te dice qué formato del Studio le conviene (tarjetas, infografía, audio, etc.).
- Contesta el test así: `1b 2d 3- 4a…` (el guion es en blanco). Te corrige y te explica los fallos.
- `Otra ronda`: otro test de la misma norma.
- `Simulacro`: una vez por semana en cada cuaderno.
- `Inglés`, en su cuaderno: dos veces por semana.

## 4. Si te recomienda un formato del Studio

El chat no puede crear audios, infografías ni cuestionarios por sí solo. Te dará un bloque **«▶ STUDIO → botón»**: pulsa ese botón en el panel Studio, deja marcada solo la norma que te indique, pulsa el lápiz y pega el texto.

## Antes de memorizar

- **Contrasta con el BOE consolidado** cualquier dato que vayas a memorizar. Si NotebookLM no puede darte la cita literal, no lo estudies.
- **Cupos diarios aproximados del plan gratuito:** 50 mensajes de chat, 3 resúmenes de audio y 10 cuestionarios. Cada sesión de estudio gasta pocos mensajes porque lo hace todo en una sola respuesta.

## Qué hay en esta carpeta

| Fichero | Qué haces con él |
|---|---|
| `PROMPT_MAESTRO.md` | Lo copias (paso 2). |
| `01_radiografia_tribunal.md` | Lo subes como fuente. Es el análisis completo de cómo pregunta el tribunal, por si quieres consultarlo. |
| `02_preguntas_oficiales_anotadas.md` | Lo subes como fuente. Son las 180 preguntas oficiales de 2023 y 2025 con su clave y su anotación. |
| `datos/` | Datos y estadísticas de los que salen las dos guías. No hace falta tocarlo. |
