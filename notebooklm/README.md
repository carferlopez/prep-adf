# Estudiar con NotebookLM en 3 pasos

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

## 2. Estudia cada norma con un informe interactivo

1. En el panel de fuentes, marca la norma que vas a estudiar y las dos guías.
2. Abre Studio → Informes → informe interactivo.
3. Pega el **prompt 1** de `PROMPT_MAESTRO.md` cambiando solo la primera línea: `NORMA: Ley 39/2015, del Procedimiento Administrativo Común`.

NotebookLM decide el mejor formato para cada parte de la norma (tarjetas, infografías, tablas comparativas, explicaciones, minitests) y cierra con un test final de 15 preguntas al estilo del tribunal y un repaso exprés.

Para repasar un bloque entero, marca todas sus normas y escribe `NORMA: todas las fuentes marcadas`.

## 3. Simulacro semanal en el chat (opcional)

Pega el **prompt 2** de `PROMPT_MAESTRO.md` una vez en cada cuaderno: Chat → icono de ajustes → «Configurar chat» → «Personalizado». Después escribe:

- `Simulacro`: 15 + 3 preguntas del bloque en 15 minutos.
- Tus respuestas, así: `1b 2d 3- 4a…` (el guion es en blanco). Te corrige con Aciertos − Errores/3 y te explica los fallos.
- `Inglés`, en su cuaderno: dos veces por semana.

## Antes de memorizar

- **Contrasta con el BOE consolidado** cualquier dato que vayas a memorizar. Si NotebookLM no puede darte la cita literal, no lo estudies.
- **Cupos diarios aproximados del plan gratuito:** 50 mensajes de chat, 3 resúmenes de audio y 10 cuestionarios.

## Qué hay en esta carpeta

| Fichero | Qué haces con él |
|---|---|
| `PROMPT_MAESTRO.md` | Lo copias: el prompt 1 en cada informe (paso 2) y el prompt 2 en el chat (paso 3). |
| `01_radiografia_tribunal.md` | Lo subes como fuente. Es el análisis completo de cómo pregunta el tribunal, por si quieres consultarlo. |
| `02_preguntas_oficiales_anotadas.md` | Lo subes como fuente. Son las 180 preguntas oficiales de 2023 y 2025 con su clave y su anotación. |
| `datos/` | Datos y estadísticas de los que salen las dos guías. No hace falta tocarlo. |
