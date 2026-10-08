# Prompts para NotebookLM (Gemini Notebook) · Examen Adif 2026

Prompts listos para copiar y pegar. Se apoyan en dos fuentes que debes subir al cuaderno:

- **«Radiografía del Tribunal»**: el archivo `01_radiografia_tribunal.md`. Si tu versión permite renombrar fuentes, ponle este nombre; si no, los prompts la reconocen por el nombre del archivo.
- **«Preguntas oficiales anotadas»**: el archivo `02_preguntas_oficiales_anotadas.md`.

Junto a ellas van las normas en texto oficial (BOE consolidado, Declaración sobre la Red, etc.). Todos los prompts obligan a citar el texto literal de la norma.

**Marcadores que debes sustituir:** `[TEMA]` (por ejemplo, «Control interno de la IGAE»), `[NORMA]` (por ejemplo, «Ley 47/2003, General Presupuestaria»), `[N]` (número de preguntas o tarjetas). Algunos prompts tienen marcadores propios, explicados en cada caso.

**Límites que se han tenido en cuenta**

| Dónde | Límite | Estado | Qué se ha hecho |
|---|---|---|---|
| Instrucciones personalizadas del chat («Configurar chat» → «Personalizado») | 10.000 caracteres | Confirmado: subió de 500 a 10.000 en diciembre de 2025 | P0 largo de unos 3.200 caracteres, más una versión de menos de 500 por si tu cuenta conserva el límite antiguo |
| Texto de personalización de Cuestionario, Tarjetas, Informes y Resumen de audio del Studio | Desconocido | No confirmado | Versión corta de menos de 1.000 caracteres para el Studio, más una versión larga para el chat |
| Mensaje normal del chat | Desconocido | No confirmado | Prompts de chat de menos de 2.000 caracteres |

Desde el 16 de julio de 2026, NotebookLM se llama **Gemini Notebook**. Los cuadernos y los enlaces siguen funcionando y los menús pueden aparecer con el nombre nuevo.

**Regla para el Studio (Cuestionario, Tarjetas, Informes, Audio):** el Studio trata como temario todas las fuentes marcadas. Antes de generar, **desmarca** «Radiografía del Tribunal» y «Preguntas oficiales anotadas» y deja marcada solo la norma del tema. Los prompts cortos ya llevan las reglas de estilo esenciales y prohíben preguntar sobre las guías por si se te olvida desmarcarlas. En el chat, en cambio, deja las dos guías marcadas.

---

## P0. Instrucciones personalizadas del chat

**Dónde pegarlo:** panel Chat → icono de ajustes (arriba a la derecha) → «Configurar chat» → estilo «Personalizado». Hazlo una vez por cuaderno y comprueba que sigue ahí al abrir una sesión nueva. Longitud de respuesta: «Más larga».

```text
ROL
Eres mi preparador del examen de Adif (OEP 2026, Técnico / Cuadro Técnico, perfil Gestión). Respondes en español de España, claro y directo.

FUENTES Y PRIORIDAD
1. Manda el texto literal de las normas y documentos oficiales del cuaderno (BOE consolidado, Declaración sobre la Red, Estatutos, Canal Ético, temario). De ahí sale todo dato: plazos, órganos, cifras, listas, requisitos.
2. «Radiografía del Tribunal» (01_radiografia_tribunal) fija el ESTILO: plantillas, distractores, proporciones, formato y trampas. No es materia de examen: nunca hagas preguntas sobre ella ni sobre sus porcentajes.
3. «Preguntas oficiales anotadas» (02_preguntas_oficiales_anotadas) son ejemplos reales con Q-id para imitar el estilo. No las copies como preguntas nuevas salvo que te lo pida.
4. Si una guía de estilo contradice la norma, gana la norma y me avisas. Si un dato no está en las fuentes, escribe «No consta en las fuentes» y no lo completes de memoria.

CÓMO GENERAS PREGUNTAS
- Antes de redactar, localiza el fragmento literal de la norma. La correcta lo copia literal o casi literal.
- Pregunta datos examinables: quién (órgano competente), cuánto (plazos, cifras), listas cerradas (cuál NO / cuál sí), requisitos, derechos y deberes, definiciones y denominaciones, regla general y excepción, ámbito y efectos.
- 4 opciones (a-d) y una sola correcta. Nunca «todas/ninguna de las anteriores».
- Mezcla: unas 2/3 preguntas directas «¿…?», 1/6 frases a completar «:» y 1/8 «señale la afirmación CORRECTA / INCORRECTA»; en total, 3 de cada 4 acaban en «?». Alrededor del 15 % negativas, con NO o INCORRECTA en mayúsculas.
- Abre citando la norma en 2 de cada 3 preguntas («Según la Ley 47/2003, General Presupuestaria, ¿…?»).
- Distractores reales de la misma norma o de la vecina: órgano cambiado, cifra contigua o de la excepción, elemento de la lista vecina, excepción convertida en regla, condición añadida o suprimida, absoluto añadido, inversión mínima («no», «sin», «salvo que»). Como mucho uno absurdo.
- En las negativas, las tres opciones que no se marcan son frases verdaderas y literales de la norma.
- Opciones paralelas y de longitud parecida. La correcta no siempre es la más larga ni siempre la que no tiene absolutos. Reparte la letra correcta entre a, b, c y d.
- No reveles la respuesta en el enunciado. Comprueba que ningún distractor sea también verdadero.

FORMATO DE CADA PREGUNTA
Pregunta [n] · [norma] · [artículo] · Plantilla [P01-P18] · Nivel [1-3]
[Enunciado]
a) …
b) …
c) …
d) …
Respuesta: [letra]
Explicación: [1-3 frases]. Cita literal: «[texto exacto]» ([artículo], [norma]).
Por qué fallan las demás: a) [tipo de distractor]: [motivo]; b) …; c) …
Tipo de trampa: [nombre usado en la Radiografía]
Nivel: [1-3]
En las negativas, en vez de «Por qué fallan las demás», pon «Por qué las demás son verdaderas», con su cita.

Si te pido un test «sin soluciones», da solo enunciados y opciones, y no muestres las soluciones hasta que te dé mis respuestas.

CÓMO EXPLICAS
- Primero la regla en una frase sencilla, después la cita literal y al final la trampa del tribunal.
- Separa siempre lo que dice la norma de lo que es una pista de examen.
- Si la norma ha cambiado, dilo y usa la versión vigente.
```

**Versión corta** (menos de 500 caracteres; solo si el campo no admite la larga):

```text
Preparador del examen Adif; español de España. Datos solo del texto literal de las normas; si no consta, dilo. Estilo según «Radiografía del Tribunal» e imitando «Preguntas oficiales anotadas»; nunca preguntes sobre ellas. 4 opciones, una correcta, distractores reales de la misma norma. Cada pregunta: respuesta, cita literal y artículo, por qué fallan las otras, trampa y nivel 1-3.
```

---

## P1. Cuestionario de [N] preguntas en el chat, con autocomprobación

**Dónde pegarlo:** en el chat, con marcadas la norma del tema, «Radiografía del Tribunal» y «Preguntas oficiales anotadas».

```text
Genera [N] preguntas tipo test sobre [TEMA] de la [NORMA], al estilo del tribunal de Adif. Los datos salen solo del texto de la [NORMA]. El estilo, de «Radiografía del Tribunal» (algoritmo de la sección 3, plantillas de la 4, distractores de la 5) y de los ejemplos de «Preguntas oficiales anotadas» de la misma norma o de una parecida.

PASO 1. Elige [N] datos examinables y preséntalos en una tabla: n.º | artículo | tipo de dato (órgano, plazo, lista, requisito, regla/excepción, definición, denominación, ámbito, efecto) | cita literal (máximo 30 palabras). Empieza por las zonas calientes de la Radiografía (sección 6.3) si son de esta norma. No repitas un artículo más de dos veces.

PASO 2. Redacta las preguntas con el formato obligatorio de la sección 9 de la Radiografía. Reparto:
- unas 2/3 preguntas directas, 1/6 frases a completar y 1/8 «señale la afirmación CORRECTA / INCORRECTA»;
- alrededor del 15 % negativas (NO o INCORRECTA en mayúsculas), con tres opciones verdaderas literales;
- niveles 1/2/3 cerca de 40/50/10 %;
- letras correctas repartidas, nunca más de tres iguales seguidas;
- la correcta, la más larga como mucho en el 40 % de las preguntas.

PASO 3. Autocomprobación. Tabla: n.º | ¿cita localizada en la norma? | ¿una sola correcta? | ¿algún distractor también verdadero? | arquetipos de los distractores | letra | nivel. Debajo, el recuento de letras, negativas y niveles. Si una pregunta falla, reescríbela y muestra la versión corregida.

Si un dato no está en la [NORMA], escribe «No consta en las fuentes». No hagas preguntas sobre las guías de estilo.
```

**Variante modo examen:** añade al final «Primero dame solo los enunciados y las opciones, sin la tabla del paso 1. Cuando te escriba mis respuestas (por ejemplo, 1b 2d 3-), corrige con Aciertos − Errores/3, muestra las soluciones completas y deja la autocomprobación para el final».

---

## P2. Personalizar el Cuestionario del Studio

**Dónde pegarlo:** Studio → Cuestionario → lápiz (personalizar). Antes, en el panel de fuentes, desmarca «Radiografía del Tribunal» y «Preguntas oficiales anotadas» y deja solo la norma. Dificultad: media o difícil. Número de preguntas: el máximo que te ofrezca. Idioma: español, si aparece la opción.

```text
Test al estilo del tribunal de Adif sobre [TEMA] de la [NORMA]. Solo datos literales de la norma: órganos competentes, plazos y cifras, listas cerradas, requisitos, reglas con sus excepciones, definiciones. Enunciados que abren «Según la [NORMA], ¿…?». 4 opciones paralelas y una correcta, casi literal. Distractores reales de la misma norma: otro órgano, una cifra contigua o la de la excepción, un elemento de la lista vecina, una excepción convertida en regla, un absoluto añadido. Alrededor del 15 % negativas, con NO o INCORRECTA en mayúsculas. Nunca «todas/ninguna». La explicación cita el texto literal y el artículo. Si «Radiografía del Tribunal» o «Preguntas oficiales anotadas» están marcadas, úsalas solo como estilo: no preguntes nada sobre ellas.
```

**Versión larga (chat):** usa P1.

---

## P3. Tarjetas de datos examinables

**Dónde pegarlo (versión Studio):** Studio → Tarjetas → lápiz. Antes, desmarca «Radiografía del Tribunal» y «Preguntas oficiales anotadas» y deja solo la norma.

```text
Tarjetas de datos examinables de la [NORMA], tema [TEMA], para el examen de Adif. Una idea por tarjeta. Anverso: pregunta corta (¿quién…?, ¿qué plazo…?, ¿cuántos elementos tiene la lista y cuáles son?, ¿cuál es la excepción?, ¿cómo se denomina…?). Reverso: el texto literal de la norma y el artículo. Prioriza órganos competentes, plazos y cifras, listas cerradas completas, reglas con sus excepciones y pares que se confunden (el dato correcto frente al que se suele confundir). No hagas tarjetas sobre «Radiografía del Tribunal» ni sobre «Preguntas oficiales anotadas».
```

**Dónde pegarlo (versión larga):** en el chat, con las tres fuentes marcadas. Sirve para exportar las tarjetas a Anki u otra aplicación.

```text
Crea [N] tarjetas de datos examinables de la [NORMA] sobre [TEMA], para el examen de Adif.

Qué datos elegir: los tipos que más pregunta el tribunal según «Radiografía del Tribunal» (sección 2.5): órgano competente, intruso en listas, plazos, requisitos, derechos y deberes, definiciones y denominaciones, regla y excepción. Da prioridad a lo que ya ha caído en «Preguntas oficiales anotadas» (indica el Q-id) y a las zonas calientes de la sección 6.3.

Tipos de tarjeta que debes incluir:
1. Dato simple: «¿Quién…?», «¿Qué plazo…?».
2. Lista cerrada: «¿Cuántos elementos tiene y cuáles son?».
3. Regla y excepción: «¿Cuál es la regla? ¿Y sus excepciones, con sus cifras?».
4. Par confundible: «X frente a Y: ¿qué diferencia hay?» (por ejemplo, el órgano que consulta en un procedimiento frente al que consulta en otro).
5. Calificativo exacto: la cláusula completa, sin quitar palabras como «inmediata y directa» o «previamente».

Salida: una tabla con estas columnas: Anverso | Reverso (texto literal) | Artículo | Tipo de dato | Trampa que previene (nombre usado en la Radiografía) | Q-id si ya cayó.
Después, las mismas tarjetas en formato «anverso;reverso», una por línea, para importarlas.
Si un dato no consta en la [NORMA], no lo incluyas.
```

---

## P4. Guía de estudio de una norma orientada al tribunal

**Dónde pegarlo (versión Studio):** Studio → Informes → «Crea el tuyo». Deja marcada solo la norma.

```text
Guía de estudio de la [NORMA] para el examen tipo test de Adif. Usa solo el texto de la norma: cada dato, con su cita literal y su artículo. Apartados: 1) Quién: tabla órgano → competencia. 2) Cuánto: tabla de plazos, cifras y porcentajes. 3) Listas cerradas: número de elementos y elementos literales. 4) Reglas con sus excepciones. 5) Definiciones literales. 6) Pares que se confunden (dato correcto frente a dato parecido de otra lista o artículo). 7) Diez trampas probables: órgano cambiado, cifra de la excepción, elemento de la lista vecina, absoluto añadido, calificativo suprimido. Estilo de tablas y viñetas, sin relleno. No hables de «Radiografía del Tribunal» ni de «Preguntas oficiales anotadas».
```

**Dónde pegarlo (versión larga):** en el chat, con las tres fuentes marcadas.

```text
Prepárame una guía de estudio de la [NORMA], centrada en [TEMA] (o en toda la norma si pongo «completa»), pensada para el test de Adif. Los datos salen solo del texto de la norma, cada uno con su artículo y su cita literal (si es larga, el fragmento decisivo entre comillas).

Estructura:
1. Mapa rápido: títulos o capítulos que contienen datos examinables (máximo 10 líneas).
2. QUIÉN: tabla órgano o sujeto → qué hace (aprueba, consulta, eleva, supervisa, nombra) → artículo.
3. CUÁNTO: tabla de plazos, cifras, porcentajes y umbrales → desde cuándo se cuentan → artículo. Marca las cifras de las excepciones.
4. LISTAS CERRADAS: número de elementos y elementos literales. Al lado, la lista vecina con la que se suele confundir.
5. REGLAS Y EXCEPCIONES: regla, excepciones literales y fórmulas como «con carácter general», «salvo» o «en todo caso».
6. DEFINICIONES Y DENOMINACIONES literales, y los nombres casi iguales con los que se confunden.
7. PARES CONFUNDIBLES: tabla dato correcto | dato que se confunde | cómo distinguirlos.
8. LO QUE YA PREGUNTÓ EL TRIBUNAL: según «Preguntas oficiales anotadas», los Q-id de esta norma, qué dato preguntaron y qué trampa usaron. Añade si es zona caliente según la sección 6.3 de «Radiografía del Tribunal».
9. TRAMPAS PROBABLES: diez distractores que el tribunal podría fabricar con esta norma, siguiendo las recetas de la sección 5 de la Radiografía, cada uno con la forma de detectarlo.
10. DIEZ PREGUNTAS DE CONTROL al estilo del tribunal, con el formato de la sección 9 de la Radiografía.

Si un apartado no tiene contenido en la norma, dilo y pasa al siguiente.
```

---

## P5. Simulacro con la estructura real y corrección Aciertos − Errores/3

**Dónde pegarlo:** en el chat, con marcadas las normas de los dos bloques y las dos guías. Marcadores propios: `[NORMAS GENERAL]` (lista de normas del Conocimiento General) y `[NORMAS ESPECÍFICO]` (lista de normas del Específico de Gestión, por ejemplo LGSS, Estatuto de los Trabajadores y Ley 47/2003).

```text
Hazme un simulacro con la estructura real del examen de Adif de 2025 (ver «Radiografía del Tribunal», secciones 1 y 3).

BLOQUE 1 · CONOCIMIENTO GENERAL: 15 preguntas + 3 de reserva (16-18), sobre [NORMAS GENERAL]. Una pregunta por norma y como mucho dos de la misma. Reparte en tercios: sector ferroviario y documentos de Adif, Derecho administrativo y empleo público, y materias transversales. Estilo General: enunciados cortos, la mitad acabados en «:», casi todas de nivel 1-2.

BLOQUE 2 · CONOCIMIENTO ESPECÍFICO: 15 preguntas + 3 de reserva (16-18), sobre [NORMAS ESPECÍFICO]. Una norma dominante con alrededor del 40 % de las preguntas. Estilo Gestión: cabecera completa de la norma y, en casi la mitad, el artículo citado. Reservas algo más difíciles (nivel 3).

Reglas: datos solo del texto literal de las normas; estilo y distractores según la Radiografía y los ejemplos de «Preguntas oficiales anotadas»; alrededor del 15 % negativas; letras correctas repartidas; ninguna pregunta copiada de las oficiales.

FASE 1. Dame solo los enunciados y las opciones, numerados 1-18 en cada bloque, sin soluciones. Indica el tiempo: 15 minutos por bloque.

FASE 2. Cuando te escriba mis respuestas (por ejemplo, G1b G2- … E1c …, donde «-» es en blanco), corrige:
- por bloque: aciertos, errores, en blanco y nota = Aciertos − Errores/3, sobre las 15 ordinarias (las reservas, aparte);
- total sobre 30 y su equivalencia en 120 puntos (4 por pregunta), comparada con el mínimo del 40 % (12 aciertos netos);
- cada fallo y cada blanco con el formato de la sección 9 de la Radiografía (cita literal y artículo, por qué fallan las demás y tipo de trampa);
- al final, mis tres tipos de trampa más repetidos y qué estudiar primero.
```

---

## P6. Análisis de mis fallos, con explicación tipo Feynman

**Dónde pegarlo:** en el chat, con las tres fuentes marcadas. Pega debajo tus fallos con este formato: pregunta, opciones, mi respuesta y la correcta.

```text
Analiza mis fallos de abajo como un profesor que explica con el método Feynman. Para cada pregunta:

1. Qué dice la norma: cita literal y artículo, sacados de la fuente oficial. Si no consta, dilo.
2. Explicación sencilla: la regla en dos o tres frases, como si se la contaras a alguien que no sabe Derecho, con un ejemplo o una analogía cotidiana.
3. Por qué me engañó la opción que marqué: qué tipo de distractor era según «Radiografía del Tribunal» (sección 2.7 y trampas T1-T16 de la sección 7) y qué palabra o dato la delataba.
4. Regla de detección: una frase que pueda aplicar en el examen.
5. Pregunta gemela: una pregunta nueva sobre el mismo dato, al estilo de «Preguntas oficiales anotadas», con la solución oculta al final.

Después de todas las preguntas:
- Tabla resumen: n.º | norma y artículo | tipo de trampa | ¿fallo de memoria, de comprensión o de lectura?
- Mi patrón de error: las 2-3 trampas que más se repiten.
- Tres acciones concretas para la próxima sesión (qué tarjetas hacer y qué artículos releer).

MIS FALLOS:
[pega aquí tus preguntas falladas]
```

---

## P7. Test de inglés al estilo del tribunal

**Dónde pegarlo:** en el chat, con marcadas «Radiografía del Tribunal» y «Preguntas oficiales anotadas». Las frases del test son nuevas; las fuentes solo dan el estilo.

```text
Genera [N] preguntas de inglés al estilo exacto del tribunal de Adif, siguiendo la sección 8 de «Radiografía del Tribunal» y los ítems de inglés de «Preguntas oficiales anotadas» como modelos. Las frases deben ser nuevas: no copies las oficiales.

Reparto:
- 2/3 de hueco (______) y 1/3 de significado o equivalencia.
- Por tipo, aproximadamente: 28 % vocabulario por campos (transporte, trabajo, salud, tiendas, delincuencia), 26 % gramática (condicionales, wish / it's time, modales, gerundio, pasiva, conectores, inversión), 19 % reformulación o estilo indirecto, y el resto colocaciones, idioms y avisos o titulares.
- Nivel: sobre todo B1 y B2, con uno o dos C1. Inglés británico.
- Usa los enunciados literales del tribunal: «Which option is equivalent to the following sentence?», «What does this sign mean?», «Find the best answer to the following question. Q: … A: ______.», etc.

Cada frase tiene entre 8 y 15 palabras y una sola pista decisiva. La correcta es la forma de manual. Distractores: uno casi correcto (falso amigo o calco del español), uno del mismo campo incompatible con la pista y uno de otro tiempo verbal, imposible o literal. Las cuatro opciones, de la misma categoría gramatical y longitud parecida. Comprueba que solo una sea válida.

Formato de cada ítem: enunciado; a)-d); Respuesta; Explicación en español (la regla y por qué fallan las otras); Tipo de trampa (falso amigo, mismo campo, 2×2, tiempo verbal, literalidad…); Nivel MCER.
Al final: el reparto de letras y de tipos, y una lista de 10 palabras o estructuras que debo repasar.
```

---

## P8. Auditoría: que NotebookLM revise sus propias preguntas

**Dónde pegarlo:** en el chat, justo después de que haya generado preguntas, o pegando debajo las preguntas que quieras revisar. Marca la norma y las dos guías.

```text
Audita las preguntas [de tu respuesta anterior / que pego abajo] contra «Radiografía del Tribunal» (sección 3, paso 8, y sección 9) y contra el texto literal de la [NORMA]. Sé estricto: es mejor descartar una pregunta que estudiar un dato falso.

Para cada pregunta, una fila de esta tabla:
n.º | ¿la cita literal existe en la norma y respalda la correcta? (sí/no + artículo) | ¿una sola correcta? | ¿algún distractor también es verdadero? (cuál y por qué) | arquetipos de los distractores (nombres de la sección 2.7) | ¿maquetación correcta? (opciones paralelas, NO / INCORRECTA en mayúsculas, sin «todas/ninguna», sin pista en el enunciado) | veredicto: OK / CORREGIR / DESCARTAR

Después:
1. Recuento global comparado con la Radiografía: letras correctas, porcentaje de negativas, niveles, cuántas veces la correcta es la más larga y cuántas opciones con absoluto son correctas.
2. Las preguntas marcadas CORREGIR, reescritas con el formato de la sección 9 y su cita literal.
3. Las preguntas marcadas DESCARTAR, con el motivo.

Comprueba que ninguna pregunta trate sobre las guías de estilo ni copie una de «Preguntas oficiales anotadas».
```

---

## P9. Resumen de audio centrado en datos examinables

**Dónde pegarlo:** Studio → Resumen de audio → personalizar (lápiz). Antes, desmarca las dos guías y deja solo la norma. Idioma: español, si aparece la opción. Elige el formato y la duración que ofrezca tu versión.

```text
Resumen de audio para un opositor de Adif sobre la [NORMA], tema [TEMA]. Céntrate solo en datos examinables y dilos con el texto literal de la norma y su artículo: quién decide qué, plazos y cifras exactos, listas cerradas (di cuántos elementos tienen y nómbralos), reglas con sus excepciones y pares de conceptos que se confunden. Repite dos veces cada cifra importante. Explica las trampas típicas del tribunal: órgano cambiado, cifra de la excepción, elemento de la lista vecina y absoluto añadido. Termina con un repaso rápido de los diez datos clave. No comentes «Radiografía del Tribunal» ni «Preguntas oficiales anotadas».
```

No hay versión de chat: el audio solo se genera en el Studio. Si el campo corta el texto, quita la frase de las trampas típicas.

---

## Ciclo recomendado con estos prompts

1. **P4** (guía de la norma) → 2. **P3** (tarjetas) → 3. **P1** o **P2** (test del tema) → 4. **P8** (auditoría de las preguntas generadas) → 5. **P6** (análisis de fallos) → 6. **P5** (simulacro semanal). **P9** para repasar mientras te desplazas y **P7** dos veces por semana para el inglés.

Verifica siempre contra el BOE consolidado cualquier dato que vayas a memorizar.
