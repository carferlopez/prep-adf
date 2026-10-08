# Cómo usar este material en NotebookLM (Gemini Notebook)

Material para preparar el test de Adif (OEP 2026, Técnico / Cuadro Técnico, perfil Gestión) con NotebookLM. Desde el 16 de julio de 2026 la herramienta se llama **Gemini Notebook**: los cuadernos y los enlaces siguen funcionando y algunos menús pueden aparecer con el nombre nuevo.

## Qué hay en la carpeta

| Archivo | Qué es | ¿Se sube al cuaderno? |
|---|---|---|
| `01_radiografia_tribunal.md` | **«Radiografía del Tribunal»**: cómo pregunta el tribunal (estadísticas, algoritmo, plantillas, distractores, trampas, mapa de contenidos, inglés y estrategia). Es la especificación de estilo. | Sí |
| `02_preguntas_oficiales_anotadas.md` | **«Preguntas oficiales anotadas»**: las 180 preguntas oficiales (Q1–Q180) con su anotación y la clave oficial cuando existe (las reservas de 2023 no la tienen). | Sí |
| `03_prompts_notebooklm.md` | Prompts P0–P9 listos para pegar. | No: es para ti |
| `README.md` | Esta guía. | No |
| `datos/` | Las 180 preguntas con su anotación en JSON y las estadísticas que respaldan las cifras de la Radiografía. | No |

## 1. Qué fuentes subir

1. **Las dos guías:** `01_radiografia_tribunal.md` y `02_preguntas_oficiales_anotadas.md`. Si tu versión permite renombrar fuentes, llámalas «Radiografía del Tribunal» y «Preguntas oficiales anotadas», que es como las nombran los prompts. Los Markdown (.md) se admiten según la documentación de la versión Enterprise; que funcionen en la versión gratuita solo lo dicen terceros. Si un .md no carga, cámbiale la extensión a .txt o pega el contenido en un documento de Google Docs.
2. **El texto oficial de cada norma:** el **BOE consolidado** en PDF con texto (no escaneado), descargado de la sección de legislación consolidada del BOE. Pon la fecha de consolidación en el nombre de la fuente (por ejemplo, «LGSS RDLeg 8-2015 · consolidado 2026-09»).
3. **Los PDF de tu temario** de Adif, si son PDF con texto.
4. **La Declaración sobre la Red vigente** y, si ya está publicada, la del año siguiente (en 2025 el tribunal usó la DR 2026). Añade también el Estatuto de Adif y el de ADIF-Alta Velocidad, y los documentos del Canal Ético y antifraude si están en tu temario.

Límites del plan gratuito según la ayuda de Google (consultada por buscador en octubre de 2026): 100 cuadernos, **50 fuentes por cuaderno**, hasta 500.000 palabras o 200 MB por fuente y 50 consultas de chat al día. `02_preguntas_oficiales_anotadas.md` tiene unas 42.000 palabras, muy por debajo del límite. Los PDF que son solo imagen o están protegidos pueden fallar (esto no está confirmado).

## 2. Cómo organizar los cuadernos

Es mejor tener pocos cuadernos por bloque y, en cada sesión, dejar marcada solo la norma que estudias:

| Cuaderno | Fuentes |
|---|---|
| **Adif 2026 · Específico Gestión** | LGSS, Estatuto de los Trabajadores, Ley 47/2003, el resto del temario de Gestión, 01 y 02 |
| **Adif 2026 · General** | Ley 38/2015, Declaración sobre la Red, Estatutos de Adif y ADIF-AV, LCSP, LPACAP, LRJSP, LOPDGDD, PRL, ENS, Reglamentos (UE) 402/2013 y 2018/762, LO 3/2007, Ley 4/2023, Ley 53/1984, TREBEP, 01 y 02 |
| **Adif 2026 · Inglés** | 01 y 02 (y, si quieres, material de nivel B1–B2) |
| **Adif 2026 · Otras materias** (opcional) | Ley 21/2013, RD 929/2020, Reglamento del Sector Ferroviario, Ley 19/2013 y documentos antifraude, solo si entran en el temario de 2026 |

En cada cuaderno, configura una sola vez el chat con **P0**: Chat → icono de ajustes → «Configurar chat» → «Personalizado». Es posible que tengas que volver a pegarlo en cada sesión (no está confirmado): compruébalo la primera vez.

**Regla de oro de las fuentes marcadas:**

- **En el chat**, marca la norma del tema y las dos guías.
- **En el Studio** (Cuestionario, Tarjetas, Informes y Resumen de audio), desmarca las dos guías y deja solo la norma. El Studio trata como temario todo lo marcado y podría hacerte preguntas sobre la propia Radiografía. Los prompts del Studio ya llevan las reglas de estilo esenciales.

## 3. Ciclo de estudio

Por cada norma o tema:

1. **Entender:** P4 (guía de estudio orientada al tribunal). Empieza por las zonas calientes (sección 6.3 de la Radiografía).
2. **Memorizar:** P3 (tarjetas de datos examinables). Repasa las tarjetas falladas al día siguiente, a los 3 días y a los 7.
3. **Practicar:** P1 en el chat (más control y explicaciones con cita) o P2 en el Studio (más rápido e interactivo).
4. **Auditar:** P8 sobre las preguntas generadas. Descarta las que no tengan cita literal o que tengan dos respuestas defendibles.
5. **Corregir:** P6 con tus fallos. Anota el tipo de trampa en la que caes más.
6. **Simular:** P5 una vez por semana, con 15 + 3 preguntas de General y 15 + 3 de Específico, corregido con Aciertos − Errores/3.
7. **Extras:** P9 (audio) para repasar fuera de la mesa y P7 (inglés) dos veces por semana.

Orden de las normas: el plan de prioridades de la sección 6.6 de la Radiografía, ajustado al temario oficial de las bases de 2026.

## 4. Limitaciones

- **La IA se equivoca.** Antes de memorizar un dato, compara la cita con el **BOE consolidado** vigente. Si no puedes localizar la cita literal, no estudies ese dato.
- **Las normas cambian.** Las preguntas oficiales de 2023 y 2025 pueden apoyarse en redacciones ya modificadas (la propia Radiografía señala referencias desfasadas). Manda siempre el texto vigente.
- **La Radiografía se basa en 126 preguntas de conocimientos y 54 de inglés.** Los porcentajes orientan, pero no predicen. Las heurísticas de examen (absolutos, opción más larga, posición) no sustituyen al estudio y el tribunal puede cambiarlas.
- **Límites no confirmados:** el tamaño máximo del texto de personalización del Studio (por eso sus prompts tienen menos de 1.000 caracteres), si las instrucciones del chat se aplican al Studio y los cupos diarios de audio y tarjetas. Si un prompt del Studio se corta, usa su versión de chat.
- **Los nombres de los menús** pueden variar con el cambio a Gemini Notebook y con las actualizaciones de la aplicación.
