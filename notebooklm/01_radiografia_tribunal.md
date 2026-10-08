# Radiografía del Tribunal de Adif

**Fuente de estilo para generar preguntas · OEP 2026, Técnico / Cuadro Técnico, perfil Gestión**

Corpus: **180 preguntas oficiales** (126 de conocimientos y 54 de inglés) de tres cuadernillos de Adif; 162 tienen clave oficial (faltan las reservas de 2023).

| Clave | Cuadernillo | Conocimientos | Q-id |
|---|---|---|---|
| T23 | PNI23/03 Técnico 2023 (temario común, incluido Técnico de Gestión) | 36 (30 + 6 reservas) | Q19–Q54 |
| AV23 | PNI23/04 Técnico Alta Velocidad 2023 (temario común) | 36 (30 + 6) | Q73–Q108 |
| Gen25 | PNI25/02 Mando Intermedio y Cuadro 2025, Conocimiento General | 18 (15 + 3) | Q127–Q144 |
| Téc25 | PNI25/02, Específico de perfiles técnicos | 18 (15 + 3) | Q145–Q162 |
| Ges25 | PNI25/02, Específico del Área de Gestión | 18 (15 + 3) | Q163–Q180 |
| Inglés | Los tres cuadernillos | 54 (45 + 9) | Q1–Q18, Q55–Q72, Q109–Q126 |

Cada pregunta se cita por su **Q-id**. El texto completo, la clave y la anotación de cada una están en la fuente **«Preguntas oficiales anotadas»** (`02_preguntas_oficiales_anotadas.md`).

---

## 0. Para qué sirve y cómo debe usarlo la IA

Este documento es una **especificación de estilo**: describe cómo elige el tribunal la norma y el dato, y cómo redacta enunciado, correcta y distractores, para que una IA (NotebookLM / Gemini Notebook) genere preguntas, tarjetas y simulacros indistinguibles de los oficiales.

Reglas para la IA, por orden de prioridad:

1. **El texto literal de la norma manda.** Todo dato sale de las fuentes oficiales cargadas (BOE consolidado, Declaración sobre la Red, Estatuto, documentos de Adif). Si esta guía y la norma discrepan, gana la norma y se avisa.
2. **Esta guía fija el estilo, no el contenido.** No es materia de examen: no se hacen preguntas sobre ella.
3. **Los ejemplos oficiales (Q-id) son moldes.** No se copian como preguntas nuevas.
4. **Ningún dato se inventa.** Si un dato no está en las fuentes: «No consta en las fuentes».
5. **Cada pregunta generada lleva su cita literal** (texto exacto y artículo).

Convenciones: **[Observado]** = medido en el corpus; **[Inferido]** = conclusión o recomendación. Los rasgos de redacción los mide un script; las clasificaciones (operación, forma, distractores, literalidad, dificultad) salen de la anotación pregunta a pregunta. Grupos pequeños: un 44 % de 18 son 8 preguntas.

---

## 1. Ficha técnica del examen [Observado]

Datos literales de las instrucciones de los cuadernillos.

| Rasgo | 2023 (categoría Técnico) | 2025 (Mando Intermedio y Cuadro) |
|---|---|---|
| Estructura | 72 preguntas: psicométrico 1–18, idioma 19–36, conocimientos 37–72 | Prueba común de 54 (psicométrico 1–18, inglés 19–36, General 37–54) + Específico de perfil de 18 |
| Tiempo | 60 min para todo | 45 min la prueba común; 15 min el Específico |
| Reservas | Psicométrico 16–18; idioma 34–36; conocimientos 67–72 | 16–18, 34–36, 52–54 y 16–18 del Específico |
| Clave de las reservas | No publicada (no se usaron) | Publicada |
| Opciones | 4; «una y solo una, es correcta» | Igual |
| Puntuación | 200: psicométrico 40, idioma 40, conocimientos 120 | 200: psicométrico 40, inglés 40, General + Específico 120 |
| Mínimos | 100 puntos en total y 40 % del máximo en cada test | Igual |
| Corrección | Aciertos − Errores/3; en blanco ni suma ni resta | Igual |
| Reclamaciones | 3 días hábiles desde las plantillas | Igual |
| Perfil de Gestión | 23/28EA Técnico de Gestión (temario común) | 25/19CT Cuadro Técnico – Área de Gestión |

**[Inferido: reparto igual de puntos entre preguntas puntuables]** Conocimientos: 120 puntos / 30 preguntas = **4 puntos por pregunta**; el mínimo del 40 % son **12 aciertos netos**. Inglés: unos 2,67 puntos por pregunta; mínimo, **6 aciertos netos** de 15. Tres errores anulan un acierto.

Ritmo: **50 segundos por pregunta** en los tres casos (60 min / 72, 45 / 54, 15 / 18).

---

## 2. Radiografía cuantitativa

### 2.1 Enunciado [Observado]

| Rasgo | Total (126) | T23 | AV23 | Gen25 | Téc25 | Ges25 |
|---|---|---|---|---|---|---|
| Termina en «?» | 74 % | 67 % | 72 % | 50 % | 94 % | 94 % |
| Termina en «:» | 25 % | 31 % | 25 % | 50 % | 6 % | 6 % |
| Abre citando la norma | 66 % | 47 % | 78 % | 56 % | 83 % | 72 % |
| Cita el artículo | 17 % | 17 % | 14 % | 11 % | 0 % | **44 %** |
| Negativa | 15 % | 19 % | 11 % | 11 % | 17 % | 17 % |
| Negación en mayúsculas | 13 % | 11 % | 11 % | 11 % | 17 % | 17 % |
| Mediana de longitud (caracteres) | 168,5 | 173,5 | 168,5 | 127,5 | 170 | 214 |

Además: el 94 % menciona la norma, el 2 % termina en «…» y el más largo tiene 416 caracteres. Gestión repite la cabecera completa del ET.

### 2.2 Forma y polaridad [Observado]

| Forma | n | % |
|---|---|---|
| Pregunta directa | 84 | 66,7 % |
| Frase a completar | 22 | 17,5 % |
| Elegir la afirmación correcta | 9 | 7,1 % |
| Elegir la afirmación incorrecta | 7 | 5,6 % |
| Supuesto práctico (todos en reservas de 2023: Q49, Q54, Q103, Q104) | 4 | 3,2 % |

Polaridad: afirmativa 108 (85,7 %), negativa 18 (14,3 %). El script cuenta 19 negativas; **16 llevan la negación en mayúsculas**.

### 2.3 Opciones [Observado]

| Rasgo | Total | T23 | AV23 | Gen25 | Téc25 | Ges25 |
|---|---|---|---|---|---|---|
| Mediana de longitud (caracteres) | 58 | 59,5 | 63 | 80,5 | 42,5 | 57 |
| Correcta = la más larga | **41 %** (47/114) | 33 % | 30 % | 50 % | 33 % | **72 %** |
| Correcta = la más corta | 25 % (29/114) | 30 % | 33 % | 11 % | 22 % | 22 % |
| Preguntas con alguna opción absoluta | 28 % | 25 % | 28 % | 44 % | 17 % | 28 % |
| Opciones absolutas que eran correctas | **7/59 (12 %)** | 1/12 | 1/16 | **4/16** | 0/6 | 1/9 |

Absolutos contados: siempre, nunca, en ningún caso, exclusivamente, solo, en todo caso. Preguntas cuyas opciones comparten un inicio de 10 o más caracteres: 12 %. Preguntas con opciones numéricas: 9 %. **«Todas / ninguna de las anteriores»: 0 %.**

Por azar, cada opción acierta el 25 %: la opción absoluta acierta la mitad (12 %) y la más larga bastante más (41 %), pero ambas señales varían (en Gen25 las absolutas acertaron 4 de 16, como el azar).

### 2.4 Posición de la correcta [Observado]

| Grupo | A | B | C | D |
|---|---|---|---|---|
| Conocimientos (114 con clave) | 25 % | 26 % | 30 % | 18 % |
| T23 | 37 % | 23 % | 20 % | 20 % |
| AV23 | 20 % | 30 % | 33 % | 17 % |
| Gen25 | 28 % | 39 % | 22 % | 11 % |
| Téc25 | 17 % | 17 % | 44 % | 22 % |
| Ges25 | 22 % | 22 % | 33 % | 22 % |
| Inglés (48 con clave) | 38 % | 23 % | 19 % | 21 % |

La D sale algo menos, pero la letra dominante cambia entre cuadernillos: no es una regla.

### 2.5 Dato examinable (operación) [Observado]

| Operación | n | % |
|---|---|---|
| Órgano competente («quién») | 22 | 17,5 % |
| Intruso en una enumeración («cuál NO») | 13 | 10,3 % |
| Plazo o tiempo | 11 | 8,7 % |
| Requisito o condición | 11 | 8,7 % |
| Derecho, obligación o prohibición | 8 | 6,3 % |
| Afirmaciones mixtas · definición (se da el término) · denominación (se da la definición) · cuál sí pertenece | 7 cada una | 5,6 % cada una |
| Regla general frente a excepción | 6 | 4,8 % |
| Dato corporativo de Adif · efecto jurídico · clasificación · ámbito o sujetos | 5 cada una | 4,0 % cada una |
| Procedimiento o trámite · cifra o cuantía | 3 cada una | 2,4 % cada una |
| Otro (número de artículo, Q176) | 1 | 0,8 % |

Agrupado: listas (intruso, cuál sí pertenece, clasificación) 25 (19,8 %); quién 22 (17,5 %); cuánto (plazos y cifras) 14 (11,1 %); qué es (definición y denominación) 14 (11,1 %); condiciones y reglas (requisito, regla/excepción, efecto, derecho, ámbito, procedimiento) 38 (30,2 %); resto (afirmaciones mixtas, dato corporativo, otro) 13 (10,3 %).

### 2.6 Literalidad de la correcta [Observado]

Literal 53 (42,1 %); casi literal 38 (30,2 %); paráfrasis 20 (15,9 %); inferencia (aplicar la regla, calcular, situar en un tramo) 15 (11,9 %). **El 72 % de las correctas es texto de la norma.** Algunas paráfrasis son imprecisas (Q78, Q175), pero siguen siendo la mejor opción.

### 2.7 Arquetipos de distractor [Observado]

En las 108 afirmativas hay 324 distractores:

| Arquetipo | n | % |
|---|---|---|
| Órgano o sujeto cambiado | 52 | 16,0 % |
| Elemento de otra lista (artículo vecino, otra fase, otra figura) | 45 | 13,9 % |
| Plausible inventado | 34 | 10,5 % |
| Cifra desplazada | 34 | 10,5 % |
| Negación o inversión de la correcta | 28 | 8,6 % |
| Término parecido confundible | 22 | 6,8 % |
| Absoluto añadido | 22 | 6,8 % |
| Mezcla de conceptos | 21 | 6,5 % |
| Condición añadida o suprimida | 20 | 6,2 % |
| Ámbito ampliado o reducido | 19 | 5,9 % |
| Sentido común absurdo | 13 | 4,0 % |
| Regla y excepción invertidas | 8 | 2,5 % |
| Unidad o plazo cambiado | 4 | 1,2 % |
| Afirmación verdadera (doble respuesta) | 2 | 0,6 % |

En las 18 negativas, **los 54 distractores son afirmaciones verdaderas y literales**: la correcta es la única manipulada o ajena. Los dos distractores verdaderos de las afirmativas son justo las dos preguntas dudosas (Q21, Q37).

### 2.8 Dificultad [Observado]

| Nivel | Criterio | n | % |
|---|---|---|---|
| 1 | Dato central y literal; distractores lejanos, absolutos o absurdos | 48 | 38,1 % |
| 2 | Discriminar entre conceptos vecinos o cifras de una serie | 63 | 50,0 % |
| 3 | Dato secundario (transitoria, anexo, cifra aislada), cálculo, supuesto o número de artículo | 15 | 11,9 % |

**8 de las 21 reservas son de nivel 3 (38 %)**, frente a 7 de las 105 ordinarias (7 %).

Coherencia de la plantilla: 112 coherentes; 12 sin clave (reservas de 2023 no usadas: Q49–Q54, Q103–Q108); 2 dudosas (Q21, Q37). Otras frágiles, en 11.4.

### 2.9 Diferencias por bloque [Observado]

- **Gen25:** 15 normas en 18 preguntas (máximo 2 por norma); 12 de nivel 1 y 6 de nivel 2, ninguna de nivel 3. Tercios: 6 de ferroviario y Adif, 6 de administrativo y empleo público, 6 transversales (datos, ENS, PRL, igualdad).
- **Téc25:** concentrado (Ley 21/2013 7, RSF 6); primeros documentos internos de Adif.
- **Ges25:** solo LGSS (8), ET (6) y LGP (4). La correcta es la más larga en el 72 % porque los distractores del ET son coloquiales y cortos.
- **T23 y AV23:** unas 15 normas cada uno; ferroviario y corporativo 16 y 17 de 36; reservas con supuestos y transitorias.

Frente a la guía previa del repositorio (559 preguntas, 2022–2025; 75 % directas, 13 % negativas, D 19 %), este corpus cita más la norma (66 % frente a 52 %) y el artículo (17 % frente a 8 %), la correcta es más a menudo la más larga (41 % frente a 34 %) y hay distractores inventados (10,5 %).

---

## 3. El algoritmo del tribunal, paso a paso

**Paso 1. Norma y artículo.** Pesos en la tabla 6.1. Según la prueba que se simule:
- Tipo General (18): una pregunta por norma, máximo dos; tercios como en 2.9.
- Tipo Específico (18): una norma dominante con ~40 % (Ley 21/2013: 7; LGSS: 8), otra con ~33 % (RSF: 6; ET: 6) y el resto con 2–4.
- Tipo temario común 2023 (36): ~15 normas; ferroviario y corporativo ~45 %.

Empieza por las zonas calientes (6.3). Fechas de documentos (Q145), objeto de un real decreto (Q132) o número de artículo (Q176): máximo uno por simulacro.

**Paso 2. Dato examinable.** Pesos de la tabla 2.5 (órgano 17 %, intruso 10 %, plazo y requisito 9 %, etc.). Un artículo da un dato examinable si contiene un sujeto que actúa (quién), un número (cuánto), una enumeración cerrada (cuáles), un «salvo» o «con carácter general» (cuándo no) o una definición (qué es).

**Paso 3. Forma y polaridad.** Pregunta directa 67 %, frase a completar 17 %, elegir correcta 7 %, elegir incorrecta 6 %, supuesto 3 % (solo nivel 3 o reservas). Negativas 14 %, con intruso o afirmaciones mixtas y **NO / INCORRECTA en mayúsculas**. Cierre: «?» tres de cada cuatro; en estilo General, mitad y mitad.

**Paso 4. Plantilla.** Toma una del catálogo (sección 4). Abre citando la norma en dos de cada tres, con número y a menudo título completo. Cita el artículo en una de cada seis (en estilo Gestión, casi la mitad).

**Paso 5. Correcta.** Copia el fragmento de la norma, **literal o casi literal en al menos el 70 %**. Paráfrasis o inferencia solo si la explicación muestra el razonamiento (tramo de sanción en Q49, umbral en Q179, transitoria en Q54; Q49 y Q54 son reservas sin clave).

**Paso 6. Distractores.** Receta según el tipo de dato (sección 5). Reglas de mezcla:
- En una afirmativa, al menos dos arquetipos distintos y al menos un **casi acierto** (órgano cambiado, cifra contigua, lista vecina o término parecido).
- Como máximo uno de sentido común absurdo (4 % observado).
- Material de la misma norma o de la vecina; lo inventado debe sonar a jerga real (Q167).
- En una negativa, tres frases **verdaderas y literales** y una manipulada (una palabra, un sujeto o un «no») o ajena.

**Paso 7. Maquetación.**
- Enunciado de 120–220 caracteres (estilo General ~130; estilo Gestión ~210).
- Opciones de ~58 caracteres (General ~80; técnico ~43), paralelas, que pueden empezar igual. En las frases con «…», las opciones empiezan por «...» (Q35, Q100).
- Correcta = la más larga en torno al 40 %; la más corta en torno al 25 %.
- Letras A–D al ~25 % cada una; nunca más de tres iguales seguidas.
- Las opciones que son frases terminan en punto («Leves.», «4 meses.»).
- Absolutos sobre todo en distractores, pero alrededor de 1 de cada 8 opciones absolutas debe ser correcta (12 % observado; Q171: «Nunca.»).
- Prohibido: «todas / ninguna de las anteriores» y combinaciones de letras.

**Paso 8. Control de calidad.** (1) Cita literal y artículo localizados. (2) **Ningún distractor es también verdadero** (fallo de Q21 y Q37). (3) Cada distractor es falso por una razón explicable con la norma. (4) El enunciado no regala la respuesta. (5) En un bloque: letras repartidas, ~15 % negativas, ningún artículo más de dos veces, niveles cerca de 40/50/10 %. (6) Dato vigente; si la norma cambió, se avisa.

---

## 4. Catálogo de plantillas canónicas

Frecuencia de la operación o forma asociada (una pregunta puede encajar en varias). Ejemplos literales.

**P01. Quién.** «Según [NORMA], ¿a quién corresponde [COMPETENCIA]?» · 22/126 (17,5 %).
> Según la Ley 38/2015, ¿a quién corresponde la elaboración, aprobación y publicación de la Declaración de la Red? (Q134)

**P02. Intruso.** «Según [NORMA], ¿cuál de los siguientes [ELEMENTOS] NO se considera…?» · 13/126 (10,3 %).
> Según el Real Decreto 2387/2004 - Reglamento del Sector Ferroviario, ¿cuál de los siguientes elementos NO se considera parte de la infraestructura de vía? (Q148)

**P03. Plazo.** «En [NORMA], ¿cuál es el plazo / con qué antelación / durante cuánto tiempo…?» · 11/126 (8,7 %).
> En la Ley 39/2015, ¿cuál es el plazo para interponer un Recurso potestativo de Reposición contra una Resolución expresa? (Q89)

**P04. Requisito.** «Según [NORMA], ¿qué necesitan / qué requisitos / cuándo debe…?» · 11/126 (8,7 %).
> Según el Reglamento del Sector Ferroviario, ¿qué necesitan los agentes de transporte, cargadores y operadores de transporte combinado para solicitar capacidad de infraestructura ferroviaria? (Q154)

**P05. Derecho o deber.** «Según [NORMA], ¿a qué están obligados / cuál constituye un derecho…?» · 8/126 (6,3 %).
> Según el artículo 31 de la Ley Orgánica 3/18 de Protección de Datos Personales. ¿A qué están obligados los responsables y encargados del tratamiento? (Q98)

**P06. Elegir la CORRECTA.** «En relación con [INSTITUTO], señale la respuesta CORRECTA:» · 9/126 (7,1 %).
> En relación con el Canal Ético de Adif, señale la respuesta CORRECTA: (Q146)

**P07. Elegir la INCORRECTA.** «¿Cuál de estas afirmaciones relativas a [INSTITUTO] es INCORRECTA?» · 7/126 (5,6 %).
> ¿Cuál de estas afirmaciones relativas al aplazamiento de pago de las deudas de seguridad social es INCORRECTA? (Q177)

**P08. Denominación.** «Según [NORMA], ¿cómo se denomina [DEFINICIÓN LITERAL]?» (variante: «…nos estamos refiriendo a:», Q82) · 7/126 (5,6 %).
> Según lo dispuesto en el RD 311/2022, ¿cómo se denomina al conjunto de directrices que rigen la forma en que una organización gestiona y protege la información que trata y los servicios que presta? (Q29)

**P09. Definición.** «[NORMA] define “[TÉRMINO]” como:» · 7/126 (5,6 %).
> El Reglamento 402/2013 de la Comisión, de 30 de abril define “código práctico” como: (Q24)

**P10. Sí o no con matices.** «¿Es posible / tiene obligación / exige…?» con «Sí / No / Sí, salvo… / Sí, como regla general» · 7 preguntas (Q20, Q38, Q91, Q92, Q103, Q150, Q153).
> Según lo establecido en la Ley 9/2017, ¿es posible modificar mediante aclaración un Pliego de cláusulas administrativas particulares? (Q92)

**P11. Artículo citado y frase continuada.** «De conformidad con el artículo [N] de [NORMA], [SUJETO]…» con opciones que empiezan por «...» · cita el artículo 21/126 (17 %); cierre en «…» 2 %.
> De conformidad con el artículo 14 de la Ley 53/1984, de 26 de diciembre, de Incompatibilidades del personal al servicio de las Administraciones Públicas, los reconocimientos de compatibilidad… (Q100)

**P12. Clasificación.** «Según [NORMA], ¿de qué tipo de [PROCEDIMIENTO] será objeto [SUPUESTO CON UMBRALES LITERALES]?» · 5/126 (4,0 %).
> Según lo dispuesto en la Ley 21/2013, de 9 de diciembre, de evaluación ambiental, ¿de qué tipo de evaluación ambiental será objeto cualquier modificación de las características de un proyecto consignado en el anexo I o en el anexo II, cuando dicha modificación cumple, por sí sola, los umbrales establecidos en el anexo I? (Q77)

**P13. Ámbito.** «Según [NORMA], ¿a quién se aplica…?» · 5/126 (4,0 %).
> Según se recoge en el Real Decreto Legislativo 2/2015, de 23 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto de los Trabajadores, ¿a quién se aplica el Estatuto de los Trabajadores? (Q165)

**P14. Efecto.** «En [NORMA], ¿qué efectos produce [SITUACIÓN]?» · 5/126 (4,0 %).
> En la Ley 39/2015, ¿qué efectos produce la falta de resolución expresa en un procedimiento sancionador incoado de oficio por la Administración? (Q30)

**P15. Cuál sí pertenece.** «En [NORMA], son [CATEGORÍA] los [ACTOS] en los siguientes casos:» · 7/126 (5,6 %).
> En la Ley 39/2015, son nulos de pleno derecho los actos dictados por las Administraciones Públicas en los siguientes casos: (Q85)

**P16. Documento corporativo.** «Según [DOCUMENTO DE ADIF], ¿quiénes / en qué fecha…?» · 5/126 como operación; por norma, 8 salen de la Declaración sobre la Red y 3 de antifraude y Canal Ético.
> Según se establece en la Política corporativa de lucha contra el fraude, la corrupción y el soborno, ¿quiénes se encuentran especialmente expuestos al riesgo de fraude, corrupción y soborno? (Q160)

**P17. Supuesto práctico.** «[SUJETO] ha [HECHO]… ¿Cuál es [CONSECUENCIA]?» · 4/126, solo reservas de 2023.
> Una empresa de Comunicación ha sido sancionada con 150.000 Euros por incumplir la Ley Orgánica 3/18 de Protección de Datos Personales. ¿Cuál es el plazo de prescripción de la citada sanción? (Q49)

**P18. Número de artículo.** «Según [NORMA], ¿qué artículo regula [FIGURA]?» · 1/126. Rara.
> Según el Real Decreto Legislativo 8/2015, ¿qué artículo regula el complemento por mínimos en pensiones contributivas? (Q176)

---

## 5. Catálogo de distractores: receta según el tipo de dato

Identifica el tipo de dato de la correcta y aplica su receta. Entre paréntesis, peso del arquetipo en los 324 distractores.

**5.1 PLAZO o CIFRA**
- Serie contigua con la buena en medio (cifra desplazada, 10,5 %): 3, 4, 5 y 6 meses (Q39); 2, 3, 4 y 5 meses (Q159); artículos 58 a 61 (Q176).
- Cifras reales de otra fase o de la excepción: 10 y 15 años son excepciones de los acuerdos marco (Q84); 2 meses es la prórroga y 3 el plazo del informe de impacto ambiental (Q159); 2 meses es el plazo del contencioso (Q89).
- Mitad, doble y número redondo: «Siete y medio.», «Diez.», «Treinta.» frente a «Quince.» (Q101).
- Plazo añadido donde no hay: quince días, dos meses o un mes frente a la única sin plazo (Q35).
- Fórmula abierta: «Por tiempo indefinido.» frente a «Un mínimo de 10 años.» (Q48).
- Unidad o punto de inicio cambiados (1,2 %): meses de las pagas extra (Q172); plazos cruzados con su inicio (Q128).

**5.2 ÓRGANO o SUJETO** (órgano cambiado, 16,0 %, el arquetipo más frecuente)
- Actores del mismo ecosistema: AESF, Agencia Ferroviaria de la UE, Ministerio, Consejo de Ministros (Q47, Q134); IGAE, Tribunal de Cuentas, SNCA (Q166); Ministro de Hacienda, CDGAE, Presidente del Gobierno, Consejo de Ministros (Q169); autor, promotor, órgano sustantivo, órgano ambiental (Q155–Q157, Q162).
- Mismo órgano, otro cauce: la IGAE por los servicios de inspección de los ministerios en lugar de sus Intervenciones Delegadas (Q166).
- Sujeto plural partido (ámbito reducido, 5,9 %): solo el administrador o solo las empresas ferroviarias (Q106, reserva sin clave); «Solo tiene deber de confidencialidad el responsable.» (Q133).
- Sujeto cambiado en una frase literal (Q19, Q45).

**5.3 LISTA cerrada**
- Negativa: tres elementos literales y un intruso, que puede ser:
  - de la lista vecina (13,9 %): capas de asiento, que son superestructura (Q148); telecomunicaciones fijas entre las de electrificación (Q151); trámite de audiencia entre los modos de finalizar (Q141);
  - inventado con jerga real (10,5 %): «La fiscalización de los programas de actuación presupuestaria.» (Q167); «Publicación en el BOE de las funciones y estructura.» (Q74);
  - del mismo artículo con signo contrario: los Protocolos Generales de Actuación (Q26);
  - deformación de un elemento real: «Adaptarse a los riesgos.» (Q87);
  - obligación disfrazada de derecho: «A respetar las medidas…» (Q147).
- Afirmativa: una opción de la lista y tres del artículo contiguo (anulabilidad del art. 48 frente a nulidad del 47, Q85).
- Lista incompleta con «exclusivamente» o «solamente» frente a la completa (Q41, Q138, Q152).

**5.4 REGLA CON EXCEPCIÓN**
- Excepción convertida en regla (2,5 %): indelegables como delegables (Q42); desistimiento y prescripción como excepciones a resolver (Q20); amo de casa (Q178).
- Absoluto que borra la excepción (6,8 %): «Como días naturales en todo caso.» (Q32); «Sí, siempre.» (Q91); «Sí, en todo caso.» (Q92).
- Excepción inventada (condición añadida, 6,2 %): «…salvo autorización expresa de su superior jerárquico.» (Q100); «…salvo en los casos de fuerza mayor.» (Q142).
- La correcta es la fórmula matizada: «Sí, como regla general.» (Q20); «No, solamente cabe la corrección de errores.» (Q92).
- Contraejemplo obligatorio: si la norma no tiene excepción, la correcta es el absoluto: «Nunca.» (Q171).

**5.5 DEFINICIÓN**
- Definiciones vecinas literales: discriminación indirecta y acosos frente al art. 8 (Q76).
- Misma definición con una palabra cambiada (inversión, 8,6 %): «corresponde a la topografía natural» frente a «se ha modificado la topografía natural» (Q95); «señalización en vía» frente a «en la cabina» (Q75).
- Conceptos del mismo reglamento mezclados (6,5 %): sistema de referencia, criterio experto y registro de peligros para «código práctico» (Q24).

**5.6 DENOMINACIÓN**
- Casi homónimos de la misma ley (término parecido, 6,8 %): «Informe de evaluación ambiental.», que no existe, frente a declaración, documento de alcance e informe de impacto ambiental (Q40); evaluación de impacto o estratégica, ordinaria o simplificada (Q158).
- Etiqueta correcta con adjetivos de otra parte de la norma: «Política de seguridad técnica / operativa / organizativa» (Q29).
- Figuras reales de otros capítulos: proyecto básico, proyecto de construcción, plan de aumento de capacidad (Q36); infraestructuras coordinadas o congestionadas (Q82).
- Repetir una palabra del enunciado: «Medidas residuales.» (Q149).

**5.7 ÁMBITO o REQUISITO FORMAL**
- Ámbito ampliado o reducido: «A trabajadores de la Administración Pública.» (Q165); toda la RFIG frente a la sección fronteriza (Q127).
- Requisitos coloquiales: «Puede ser verbal siempre que haya dos testigos.» (Q168).

**5.8 DATO CORPORATIVO de Adif**
- Matriz 2×2: mes × año con el día fijo (Q145); vía × modalidad (Q146).
- Listas que difieren en un elemento (Q160).
- Dato verdadero con atribución falsa: Ley 26/2022 + CNMC (Q144 b).
- Régimen derogado: cánones en la Ley de Presupuestos (Q144 d).

---

## 6. Mapa de contenidos

### 6.1 Norma por convocatoria [Observado]

| Norma o documento | T23 | AV23 | Gen25 | Téc25 | Ges25 | Total |
|---|---|---|---|---|---|---|
| Ley 21/2013, evaluación ambiental | 3 | 3 | – | 7 | – | 13 |
| Ley 38/2015, Sector Ferroviario (LSF) | 5 | 4 | 1 | – | – | 10 |
| LO 3/2018, Protección de Datos (LOPDGDD) | 5 | 3 | 1 | – | – | 9 |
| Ley 9/2017, Contratos (LCSP) | 3 | 3 | 2 | – | – | 8 |
| Declaración sobre la Red (DR 2023 y 2026) | 2 | 4 | 2 | – | – | 8 |
| RDLeg 8/2015, LGSS | – | – | – | – | 8 | 8 |
| RDLeg 2/2015, Estatuto de los Trabajadores | – | – | – | – | 6 | 6 |
| RD 2387/2004, Reglamento del Sector Ferroviario | – | – | – | 6 | – | 6 |
| Ley 39/2015 (LPACAP) | 2 | 2 | 1 | – | – | 5 |
| Ley 40/2015 (LRJSP) | 2 | 2 | 1 | – | – | 5 |
| Ley 31/1995, PRL | 2 | 2 | 1 | – | – | 5 |
| RD 311/2022, ENS | 1 | 2 | 2 | – | – | 5 |
| Reglamento (UE) 402/2013 (evaluación del riesgo) | 2 | 2 | 1 | – | – | 5 |
| Reglamento (UE) 2018/762 (sistema de gestión de la seguridad) | 2 | 2 | 1 | – | – | 5 |
| Estatutos de Adif (RD 2395/2004) y ADIF-AV (RD 1044/2013) | 3 | 3 | 1 | – | – | 7 |
| RD 929/2020, seguridad operacional | 2 | 2 | – | – | – | 4 |
| Ley 47/2003, General Presupuestaria | – | – | – | – | 4 | 4 |
| LO 3/2007 (igualdad) y Ley 4/2023 | 1 | 1 | 2 | – | – | 4 |
| Ley 53/1984 (incompatibilidades) y TREBEP | 1 | 1 | 2 | – | – | 4 |
| Antifraude y Canal Ético de Adif | – | – | – | 3 | – | 3 |
| Ley 19/2013, Transparencia | – | – | – | 2 | – | 2 |
| **Total** | **36** | **36** | **18** | **18** | **18** | **126** |

Por bloques: ferroviario y Adif 48 (38 %); administrativo y empleo público 24 (19 %); transversales (datos, ENS, PRL, igualdad) 23 (18 %); Gestión 18 (14 %); medio ambiente 13 (10 %). **En los tres cuadernillos comunes** aparecen LSF, LOPDGDD, LCSP, DR, LPACAP, LRJSP, PRL, ENS, los dos reglamentos UE, Estatutos, igualdad e incompatibilidades.

### 6.2 Qué ha caído y qué dato se pregunta [Observado]

Formato: materia (tipo de dato) y Q-id.

- **Ley 21/2013:** quién hace cada trámite (órgano) Q96, Q155–Q157, Q162; acto o documento de cada procedimiento (denominación) Q40, Q149, Q158; qué procedimiento (clasificación) Q33, Q77; plazos Q159; Red Natura Q53; vigencia de DIA Q103.
- **LSF:** zonas y explanación Q28, Q95; DR, antelación y autor Q39, Q134; plan de contingencias Q36; acuerdos marco (regla/excepción) Q84; estudio informativo Q91; puertos, ramales, intersecciones Q50, Q51, Q108.
- **LOPDGDD:** infracciones y prescripción (clasificación, plazo) Q22, Q52, Q49; registro Q31, Q98; DPD Q88; bloqueo Q104; confidencialidad Q133; transitoria Q54.
- **LCSP:** plazos Q32, Q90; contrato menor Q38; lotes Q41; pliegos Q92, Q99; ámbito Q129; modificaciones Q142.
- **DR:** fronteras Q21; habilitaciones Q46; LZB, CTC, especializada (definiciones) Q75, Q107, Q82; explotación segura Q106; transfronterizas y cánones Q127, Q144.
- **LGSS:** irrenunciabilidad Q171; pagas Q172; accidente de trabajo Q173; prescripción Q174; acción protectora Q175; artículo Q176; aplazamiento Q177; art. 168 Q178.
- **ET:** deberes y derechos Q163, Q170; tiempo parcial Q164; ámbito Q165; despido disciplinario Q168; causas objetivas Q179.
- **RSF:** derechos de usuarios Q147; infraestructura Q148; electrificación Q151; Registro Especial Q152; candidatos Q154; inspección Q161.
- **LPACAP:** resolver Q20; silencio y caducidad Q30; nulidad Q85; reposición Q89; fin del procedimiento Q141.
- **LRJSP:** convenios Q26; delegación Q42; órganos Q74; responsabilidad Q78; potestad sancionadora Q136.
- **PRL:** EPI Q19; planificación Q44; consulta Q79; principios Q87; formación Q130.
- **ENS:** política Q29; continuidad Q81; nube Q105; objeto Q132; auditoría Q143.
- **Reglamentos UE:** 402/2013: definición Q24; significatividad del cambio Q37, Q138; organismo de evaluación Q94; documentación Q97. 2018/762: competencias Q25; alta dirección y política Q43, Q80, Q83; definición Q137.
- **Estatutos:** telecomunicaciones Q23; policía Q27; Consejo Q45; Presidente Q140. ADIF-AV: endeudamiento Q73; Presidente Q86; régimen tributario Q93.
- **RD 929/2020:** quién autoriza o supervisa Q47, Q102; conservación de datos Q48; paso a nivel Q101. **LGP:** control de la IGAE Q166, Q167; anteproyecto Q169; plurianuales Q180.
- **Igualdad:** planes Q34; discriminación directa Q76; criterios de actuación Q131; rectificación registral Q128. **Empleo público:** compatibilidad Q35, Q100; actividad privada Q139; regalos Q135. **Transparencia:** plazo y límites Q150, Q153. **Antifraude y Canal Ético:** fecha Q145; vías Q146; personal expuesto Q160.

### 6.3 Zonas calientes repetidas de 2023 a 2025 [Observado]

| Zona | 2023 | 2025 |
|---|---|---|
| Ley 21/2013: promotor, órgano sustantivo, órgano ambiental | Q96 | Q155, Q156, Q157, Q162 |
| Ley 21/2013: documento o acto de cada procedimiento | Q33, Q40, Q77 | Q149, Q158 |
| Reglamento 402/2013: significatividad del cambio | Q37 | Q138 |
| Reglamento 2018/762: política de seguridad, alta dirección y organismos | Q43, Q80, Q83 | Q137 |
| Ley 53/1984: compatibilidad (art. 14) y actividades privadas | Q35, Q100 | Q139 |
| Declaración sobre la Red: publicación y competencias | Q39, Q46 | Q134, Q144 |
| Estatuto: Consejo y Presidente | Q45, Q86 | Q140 |
| LOPDGDD: responsables y encargados | Q31, Q88, Q98 | Q133 |
| Igualdad: artículos con listas | Q34, Q76 | Q131 |
| ENS | Q29, Q81, Q105 | Q132, Q143 |
| LPACAP: resolver y fin del procedimiento | Q20, Q30 | Q141 |
| LCSP: pliegos, ámbito, modificaciones | Q92, Q99 | Q129, Q142 |
| PRL: listas de artículos | Q19, Q44, Q79, Q87 | Q130 |

**[Inferido]** Lo repetido en dos convocatorias es lo más probable en 2026: merece ficha propia.

### 6.4 Documentos corporativos de Adif

- **Declaración sobre la Red** (8) [Observado]. En 2023 se usó la DR 2023 (año del examen); en 2025, la DR 2026 (año siguiente, ya publicada). Pregunta definiciones técnicas del glosario, datos de la red, competencias de otros actores y normas de la LSF que reproduce.
- **Estatutos** (7) [Observado]. Órganos de gobierno, potestades y régimen económico; 3 de las 7 citan artículo y título completo (Q23, Q45, Q86).
- **Canal Ético, Declaración institucional y Política antifraude** (3, solo Téc25) [Observado]. Fechas en matriz, vías y modalidades, listas casi iguales: memoria pura.
- **[Inferido]** Para 2026: estudia la DR vigente en la fecha del examen y, si ya está publicada, la del año siguiente; comprueba qué edición citan las bases.

### 6.5 Evolución de 2023 a 2025 [Observado]

Del test común de 36 se pasa a General (18) + Específico (18) con tiempo propio y reservas con clave. Gestión deja el temario común, muy ferroviario, por un Específico de LGSS, ET y LGP que cita más artículos. El General es más fácil (una pregunta por norma, más absolutos). Entran los documentos internos de Adif. El inglés baja de B2 a B1.

### 6.6 Plan de estudio priorizado para Gestión 2026 [Inferido]

Parte de los pesos observados; contrasta antes con las bases. Escenarios: formato 2025 (General + Específico de Gestión) o formato 2023 (temario común).

| Prioridad | Norma o documento | Peso (de 126) | Qué dominar primero |
|---|---|---|---|
| 1 | LGSS | 8 (Ges25) | Accidente de trabajo, prescripción, aplazamiento, art. 168, pagas |
| 1 | Estatuto de los Trabajadores | 6 (Ges25) | Arts. 1, 4, 5, 12, 51, 52, 54, 55: listas, umbrales, forma del despido |
| 1 | Ley General Presupuestaria | 4 (Ges25) | IGAE y formas de control, elaboración del presupuesto, plurianuales |
| 1 | LSF y Declaración sobre la Red | 18 | DR (quién, plazos, definiciones, cánones), zonas, acuerdos marco |
| 2 | LCSP | 8 | Ámbito, plazos, contrato menor, pliegos, modificaciones |
| 2 | LPACAP y LRJSP | 10 | Silencio y caducidad, nulidad, recursos, delegación |
| 2 | LOPDGDD | 9 | Infracciones y prescripción, registro, DPD, confidencialidad |
| 2 | Reglamentos UE 402/2013 y 2018/762 | 10 | Seis criterios de significatividad, organismo de evaluación, alta dirección |
| 2 | PRL y ENS | 10 | Listas de los arts. 15, 16, 17, 19 y 33 LPRL; categorías y auditoría del ENS |
| 2 | Estatutos de Adif y ADIF-AV | 7 | Consejo, Presidente, potestades, régimen económico |
| 2 | Igualdad y empleo público | 8 | Arts. 8, 14 y 45 LOI; art. 14 Ley 53/1984; art. 54 TREBEP |
| 2 | Antifraude y Canal Ético | 3 | Fechas, vías, modalidades, personal expuesto (coste bajo) |
| 3 (2 con formato 2023) | Ley 21/2013 | 13 | Reparto de papeles, documentos, plazos |
| 3 | RD 929/2020, RSF, Ley 19/2013 | 12 | Solo si están en el temario de 2026 |

---

## 7. Trampas recurrentes

**T1. Sujeto cambiado dentro de una frase literal** (Q19, Q45, Q31). Detección: dos opciones casi idénticas salvo el sujeto. Entrenamiento: tarjetas «verbo → sujeto exacto».

**T2. Cifra desplazada en serie** (Q39, Q159, Q174, Q176). Detección: no se puede razonar; es memoria. Entrenamiento: tarjetas «dato → número» con repaso espaciado.

**T3. La cifra de la excepción como cebo** (Q84, Q159). Detección: «con carácter general» o «sin que existan circunstancias excepcionales» en el enunciado. Entrenamiento: fichas «regla / excepciones con sus cifras».

**T4. Excepción convertida en regla, o al revés** (Q42, Q20, Q178). Detección: un «salvo» que la norma no tiene, o falta uno que sí tiene. Entrenamiento: para cada regla, sus excepciones exactas.

**T5. Elemento de la lista vecina** (Q85, Q76, Q148, Q163, Q179). Detección: suena a la norma, pero ¿es de este artículo? Entrenamiento: estudiar artículos contiguos en pareja.

**T6. Inversión mínima: «no», «sin», «salvo que»** (Q131, Q34, Q143, Q129). Detección y entrenamiento: leer despacio las negaciones dentro de opciones largas.

**T7. Absoluto añadido, y el absoluto correcto** (Q23, Q41, Q133, Q175; contraejemplos Q171, Q142, Q143). Detección: sospechoso, no prueba: correcto 7 de 59 veces, y 4 de 16 en Gen25. Entrenamiento: ante cada absoluto, «¿tiene excepciones la norma?».

**T8. Calificativo amputado o añadido** (Q78, Q35, Q100, Q178). Detección: comparar con la cláusula completa; la correcta suele ser la más completa. Entrenamiento: memorizar cláusulas con sus calificativos.

**T9. Gemelas que difieren en un matiz** de ámbito, cómputo o «previstas / no previstas» (Q127, Q128, Q142, Q172, Q95). Detección: a menudo la correcta es una gemela, pero no en Q128 ni Q142 [observado, no medido]. Entrenamiento: tarjetas de «par confundible».

**T10. Denominaciones casi iguales de la misma ley** (Q40, Q158, Q29, Q82). Detección: cuatro nombres de una misma familia; fija primero el procedimiento. Entrenamiento: tablas procedimiento × documento o acto final.

**T11. Importar la regla de otra ley** (Q32: días hábiles de la LPACAP en la LCSP; Q89; Q144 con el régimen derogado). Detección: «¿es norma especial con regla propia?». Entrenamiento: fichas comparativas entre leyes.

**T12. Grupo fijo de actores** (Q155, Q156, Q157, Q162; antes Q96). Detección: quién inicia, quién hace la información pública, quién consulta para el alcance, quién analiza y formula. Entrenamiento: diagrama del procedimiento.

**T13. Negativa con verdaderas que suenan a falsas** (Q173; en Q45 es verdadera la opción de nueve a diez vocales). Detección: buscar la manipulada, no la rara. Entrenamiento: leer el artículo entero.

**T14. Intruso fabricado con jerga real** (Q167, Q74, Q44). Detección: saber cuántos elementos tiene la lista. Entrenamiento: memorizar el número de elementos de cada lista cerrada.

**T15. Matriz 2×2** (Q145, Q146; en inglés Q7, Q11, Q14). Detección: separar las dos variables y decidir cada una. Entrenamiento: tarjetas de una sola variable.

**T16. El vacío normativo nunca es la correcta.** Opciones que niegan que la norma regule, prevea o exija la materia («No aplica a ninguna categoría.», «No hay vigencia máxima.», «Este trámite no está contemplado en la Ley.»): aparecen en Q33, Q77, Q81, Q84, Q96, Q102, Q127, Q143, Q155 y Q175 y **nunca son la correcta** [Observado]. Matiz: si el enunciado propone un requisito concreto, «No» sí puede ser correcto (Q38 «No.», Q91, Q92, Q139). Entrenamiento: localizar el artículo que regula la materia.

---

## 8. Test de inglés [Observado salvo indicación]

**Estructura.** 18 preguntas por convocatoria (15 + 3 de reserva), posiciones 19–36. Enunciado mediano: 63,5 caracteres; opción mediana: 9. **38 de 54 ítems (70 %) llevan hueco** (______), Q2 incluida; 15 piden significado o equivalencia y 1 la preposición común (Q72). Única negativa: «Which option is NOT equivalent…» (Q17). Correcta: A 38 %, B 23 %, C 19 %, D 21 % (48 con clave; en T23, 9 de 15 fueron A: no es fiable). Ninguna clave errónea; Q125 es dudosa (11.4).

| Tipo | T23 | AV23 | 2025 | Total |
|---|---|---|---|---|
| Vocabulario y campo semántico | 5 | 2 | 8 | 15 (28 %) |
| Gramática | 3 | 7 | 4 | 14 (26 %) |
| Reformulación equivalente (incluido estilo indirecto) | 4 | 3 | 3 | 10 (19 %) |
| Colocaciones y preposiciones | 1 | 3 | 0 | 4 (7 %) |
| Idioms y proverbios | 2 | 1 | 0 | 3 (6 %) |
| Avisos, carteles y titulares | 0 | 1 | 2 | 3 (6 %) |
| Formación de palabras | 0 | 1 | 1 | 2 (4 %) |
| Phrasal verb, función comunicativa, registro informal | 3 | 0 | 0 | 3 (6 %) |

Niveles MCER: B1 25 (46 %), B2 23 (43 %), C1 6 (11 %). 2023, sobre todo B2; 2025, B1 tipo PET con un C1 (*Seldom*, Q123).

**Gramática recurrente:** condicionales (Q119, Q110), *wish + would* (Q67), *It’s time* + pasado (Q70); incontables y cuantificadores (Q11, Q14, Q112); modales (*had to* Q69, *didn’t need to* Q7, *would rather / had better* Q17, Q125); gerundio (Q65, Q71); pasiva personal (Q9); conectores (Q3, Q18, Q59); artículos (Q57); *not as… as* (Q122); inversión (Q123); *get used to* (Q5); estilo indirecto (Q58, Q68).

**Léxico:** delincuencia, salud, transporte, trabajo, tiendas, alojamiento, relaciones, personalidad, deporte. Inglés **británico** (*quid*, *chemist’s*, *jeweller’s*). Pares favoritos: *damage / harm / injure*; *fare / fee / price / toll*; *lose / miss / leave / drop*; *task / chore / duty / role*; *referee / umpire / judge*; *argument / discussion / chat*; *take place / take part*.

**Distractores:** (1) mismo campo semántico; (2) falso amigo o calco (*discussion*, *an advice*, *a good weather*, *the most people*); (3) cuadro 2×2 (Q7, Q11, Q14); (4) misma forma, otro significado (Q6, Q60, Q61); (5) otros tiempos verbales; (6) misma familia de palabras (Q55, Q117); (7) en las de significado: invertir, leer literal, añadir o repetir una palabra del enunciado; (8) una forma imposible (*unpatient* en Q55, *did I saw* en Q123, *fired* en Q126).

**Enunciados literales:** `Find the best answer to the following question. Q: … A: ______.` · `Which option is the best / true / correct according to the following sentence?` · `Which option is equivalent / NOT equivalent to the following sentence?` · `Which option is equivalent in informal English…?` · `Which sentence best reports Jenny’s words?` · `What does the following proverb / newspaper headline mean?` · `What does this sign / notice / sentence mean?` · `What does the speaker imply?` · `Which preposition can be used before balance, purpose and strike?`

**Receta:**
1. Dos tercios de hueco y un tercio de significado.
2. Punto evaluado según el peso: ~28 % vocabulario, 26 % gramática, 19 % reformulación; el resto, colocaciones, idioms y avisos.
3. Frase cotidiana de 8–15 palabras, en inglés británico, con **una sola pista decisiva**, a menudo en una segunda oración («I can’t find them anywhere.»).
4. La correcta es la forma de manual.
5. Distractores: uno casi correcto (falso amigo o sinónimo que no combina), uno del mismo campo incompatible con la pista y uno de otro tiempo, imposible o literal.
6. Misma categoría gramatical y longitud parecida; solo una válida; letra repartida.
7. **[Inferido]** Para 2026, sobre todo B1–B2 con uno o dos C1.

---

## 9. Reglas de generación para la IA

**HACER**
1. Localizar el fragmento literal antes de redactar.
2. Preguntar datos examinables (quién, cuánto, listas, requisitos, derechos y deberes, definiciones, regla y excepción, ámbito, efectos).
3. Abrir citando la norma en dos de cada tres preguntas.
4. Proporciones: ~2/3 preguntas directas, ~1/6 frases a completar, ~1/8 «señale la CORRECTA / INCORRECTA»; cierre en «?» tres de cada cuatro; ~15 % negativas con NO o INCORRECTA en mayúsculas.
5. Correcta literal o casi literal en al menos el 70 %.
6. Distractores reales de la misma norma o de la vecina, según la receta del tipo de dato.
7. En las negativas, tres verdaderas literales y una manipulada o ajena.
8. Opciones paralelas; correcta más larga en torno al 40 %.
9. Repartir letras y niveles (40/50/10 %).
10. Cita literal y artículo en cada explicación, y por qué falla cada distractor.
11. Avisar si la norma ha cambiado.

**NO HACER**
1. «Todas / ninguna de las anteriores» o combinaciones de letras.
2. Inventar artículos, cifras, plazos u órganos en la correcta, la cita o la explicación (los distractores inventados sí valen: paso 6).
3. Dejar dos opciones defendibles (Q21, Q37).
4. Revelar la respuesta en el enunciado.
5. Más de un distractor absurdo.
6. Correcta sistemáticamente la más larga, la única sin absoluto o la C.
7. Fechas de publicación, derogaciones o números de artículo salvo excepcionalmente.
8. Preguntas sobre esta guía o sobre «Preguntas oficiales anotadas».
9. Copiar preguntas oficiales como nuevas.
10. Mezclar en la correcta la regla de dos leyes.

**Formato obligatorio de cada pregunta**

```text
Pregunta [n] · [Norma abreviada] · [artículo] · Plantilla [P01–P18] · Nivel [1–3]
[Enunciado]
a) [opción]
b) [opción]
c) [opción]
d) [opción]
Respuesta: [letra]
Explicación: [1–3 frases]. Cita literal: «[texto exacto]» ([artículo], [norma]).
Por qué fallan las demás: a) [arquetipo]: [motivo]; b) …; c) …
Tipo de trampa: [arquetipo de la sección 2.7]
Nivel: [1–3] — [motivo]
```

En las negativas, «Por qué fallan las demás» se sustituye por «Por qué las demás son verdaderas», con la cita de cada una.

---

## 10. Ejemplos oficiales representativos

Literales del corpus; «← CORRECTA» marca la clave oficial.

```text
Q19 · PNI23/03 Técnico 2023 — Conocimientos (temario común Técnico)
Señale la opción INCORRECTA: Según la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, respecto a los equipos de protección individual:
a) Deberán utilizarse cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.
b) Los Delegados de Prevención velarán por el uso efectivo de los mismos cuando, por la naturaleza de los trabajos realizados, sean necesarios.  ← CORRECTA
c) Deberán ser proporcionados por el empresario.
d) El empresario deberá velar por el uso efectivo de los mismos cuando, por la naturaleza de los trabajos realizados, sean necesarios.
```

Negativa: tres verdaderas del art. 17.2 LPRL y una con el sujeto cambiado; la d es la gemela con el sujeto bueno. T1.

```text
Q20 · PNI23/03 Técnico 2023 — Conocimientos (temario común Técnico)
En la Ley 39/2015, ¿tiene la Administración Pública la obligación de dictar resolución expresa y notificarla en un procedimiento administrativo?
a) Sí, salvo en caso de desistimiento de la solicitud.
b) No.
c) Sí, salvo en caso de prescripción.
d) Sí, como regla general.  ← CORRECTA
```

La correcta es «como regla general»; los distractores convierten en excepciones casos que la ley resuelve con resolución declarativa. T4.

```text
Q148 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (resto perfiles técnicos)
Según el Real Decreto 2387/2004 - Reglamento del Sector Ferroviario, ¿cuál de los siguientes elementos NO se considera parte de la infraestructura de vía?
a) Los terraplenes.
b) Las capas de asiento.  ← CORRECTA
c) Los viaductos.
d) Las trincheras.
```

Intruso de la lista vecina: las capas de asiento son superestructura. T5.

```text
Q39 · PNI23/03 Técnico 2023 — Conocimientos (temario común Técnico)
Según la Ley 38/2015, ¿con qué antelación se publicará la Declaración sobre la red antes de que finalice el plazo de solicitud de capacidad de infraestructura?
a) 3 meses.
b) 6 meses.
c) 4 meses.  ← CORRECTA
d) 5 meses.
```

Serie contigua de meses: solo vale la memoria. T2.

```text
Q40 · PNI23/03 Técnico 2023 — Conocimientos (temario común Técnico)
Según lo dispuesto en la Ley 21/2013, de 9 de diciembre, de evaluación ambiental, ¿cómo se denomina al informe preceptivo y determinante del órgano ambiental con el que finaliza la evaluación de impacto ambiental simplificada?
a) Informe de evaluación ambiental.
b) Declaración de impacto ambiental.
c) Documento de alcance.
d) Informe de impacto ambiental.  ← CORRECTA
```

Cuatro denominaciones casi iguales; ordinaria termina en declaración, simplificada en informe. T10.

```text
Q84 · PNI23/04 Técnico AV 2023 — Conocimientos (temario común Técnico)
Según la Ley 38/2015, ¿con carácter general, cuál es el plazo máximo de vigencia de los acuerdos marco establecidos entre el administrador de infraestructuras ferroviarias y los candidatos sin que existan circunstancias excepcionales debidamente justificadas para ampliar dicho plazo?
a) 5 años.  ← CORRECTA
b) 10 años.
c) 15 años.
d) No hay vigencia máxima.
```

Las cifras falsas son las de la excepción y la d es vacío normativo; «con carácter general» avisa. T3 y T16.

```text
Q143 · PNI25/02 Cuadro Técnico 2025 — Conocimiento General · RESERVA
El Esquema Nacional de Seguridad establece que la auditoria de seguridad, con carácter extraordinario, deberá realizarse:
a) Siempre que no se produzcan modificaciones sustanciales en los sistemas de información, que puedan repercutir en las medidas de seguridad requeridas.
b) Siempre que se produzcan modificaciones sustanciales en los sistemas de información, que puedan repercutir en las medidas de seguridad requeridas.  ← CORRECTA
c) Cada año.
d) Nunca se ha de realizar.
```

A y B solo difieren en un «no»; C da una periodicidad falsa y D es vacío normativo. T6 y T16.

```text
Q145 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (resto perfiles técnicos)
¿En qué fecha se realizó la Declaración Institucional de lucha Contra el fraude por el Presidente de Adif?
a) 28 de octubre de 2024.  ← CORRECTA
b) 28 de noviembre de 2024.
c) 28 de octubre de 2023.
d) 28 de noviembre de 2023.
```

Matriz 2×2 mes × año con el día fijo. Nivel 3. T15.

```text
Q157 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (resto perfiles técnicos)
Según lo dispuesto en la Ley 21/2013, de 9 de diciembre, de evaluación ambiental, ¿quién realizará, en el procedimiento de evaluación de impacto ambiental ordinaria y dentro del procedimiento sustantivo de autorización del proyecto, los trámites de información pública y de consultas a las Administraciones Públicas afectadas y a las personas interesadas?
a) El autor.
b) El promotor.
c) El órgano sustantivo.  ← CORRECTA
d) El órgano ambiental.
```

Grupo fijo de actores; «dentro del procedimiento sustantivo» señala al órgano sustantivo. T12.

```text
Q167 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (Área Gestión)
Según el artículo 142 de la Ley 47/2003, General Presupuestaria, ¿cuál de los siguientes NO es una forma de control de la gestión económico-financiera a efectuar por la Intervención General de la Administración del Estado (IGAE)?
a) El ejercicio de la función interventora.
b) El control financiero permanente.
c) La auditoría pública.
d) La fiscalización de los programas de actuación presupuestaria.  ← CORRECTA
```

Intruso inventado con jerga presupuestaria; las formas de control son tres. Artículo citado (estilo Gestión). T14.

```text
Q171 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (Área Gestión)
¿Cuándo es válida la renuncia de un trabajador a los derechos que le confiere la Ley General de la Seguridad Social?
a) Nunca.  ← CORRECTA
b) Cuando lo autorice la Tesorería General de la Seguridad Social.
c) Cuando sea fruto de un acuerdo colectivo.
d) Siempre.
```

El absoluto es la correcta porque la norma no admite excepción. T7.

```text
Q169 · PNI25/02 Cuadro Técnico 2025 — Conocimiento Específico (Área Gestión)
Según la Ley 47/2003, General Presupuestaria, ¿quién eleva el anteproyecto de Ley de Presupuestos Generales del Estado al órgano al que corresponde su tramitación?
a) La Comisión Delegada del Gobierno para Asuntos Económicos.
b) El Presidente del Gobierno.
c) El Ministro de Hacienda.  ← CORRECTA
d) El Consejo de Ministros.
```

Cuatro órganos del mismo procedimiento; hay que saber el papel de cada uno. Receta 5.2.

---

## 11. Estrategia de examen

### 11.1 Valor esperado bajo Aciertos − Errores/3

Con probabilidad p de acertar, contestar vale **(4p − 1) / 3 preguntas netas**: compensa si p > 25 %.

| Opciones posibles | Acierto | Valor esperado (preguntas netas) | Puntos de conocimientos (4 por pregunta, inferido) |
|---|---|---|---|
| 4 | 25 % | 0 | 0 |
| 3 | 33 % | +0,11 | +0,44 |
| 2 | 50 % | +0,33 | +1,33 |
| 1 | 100 % | +1 | +4 |

Regla **[Inferido, del cálculo]**: si descartas al menos una opción con seguridad, contesta. Si no descartas ninguna, deja en blanco salvo que tengas una razón concreta (p > 25 %); adivinar a ciegas tiene valor cero y más varianza. Las reservas puntúan si se anula alguna pregunta: contéstalas con el mismo criterio.

### 11.2 Tiempos

Propuesta **[Inferido]**, a 50 segundos de media por pregunta:
- **Prueba común 2025** (45 min, 54 preguntas): inglés 8–10 min (ítems cortos), General ~15 min, el resto para el psicométrico.
- **Específico 2025** (15 min, 18): primera pasada de 9–10 min con lo seguro, segunda de 4 min con la regla 11.1 y un minuto para revisar la hoja.
- **2023** (60 min, 72): mismo reparto proporcional.

### 11.3 Heurísticas de último recurso, con su fuerza medida

Señales estadísticas que **no sustituyen al estudio** y cambian entre cuadernillos.

| Heurística | Fuerza medida | Dónde falla |
|---|---|---|
| Descartar el vacío normativo | 0 correctas en 10 apariciones con clave (T16) | Si el enunciado propone un requisito concreto, «No» puede ser correcto (Q38, Q91, Q92, Q139) |
| Desconfiar del absoluto | Correcto 7 de 59 (12 %) frente al 25 % del azar | Gen25: 4 de 16 (25 %); Q171, Q142, Q143 |
| Preferir la más larga | Correcta 47 de 114 (41 %) frente al 25 % | 30 % en AV23, 72 % en Ges25; la más corta acierta el 25 % |
| Evitar la D | D correcta 21 de 114 (18 %) | Señal débil; 22 % en Téc25 y Ges25 |
| Entre gemelas, una de ellas | Observado (Q19, Q95, Q127, Q172), no medido | Falla en Q128 y Q142; no siempre hay gemelas |

Orden propuesto **[Inferido]**: descarta lo que sabes falso, luego el vacío normativo, desconfía de los absolutos salvo que la norma sea tajante, prefiere la opción más completa y legal y, con dos o tres posibles, contesta. Elegir la más larga sin saber nada vale de media (4 × 0,41 − 1) / 3 ≈ +0,21 preguntas netas aquí, pero +0,07 con el 30 % de AV23: positivo y frágil.

Señales del enunciado: si cita el artículo (44 % en Gestión), asociar número y título regala la pregunta (Q98: art. 31, registro de actividades); memoriza los títulos de los artículos más preguntados. «Con carácter general» avisa de que las otras cifras son de la excepción (Q84).

### 11.4 Preguntas dudosas o impugnables y qué enseñan

- **Q21** (DR 2023): clave A (Fuentes de Oñoro/Vilar Formoso), pero Badajoz/Elvas (C) también conecta con Portugal.
- **Q37** (Reglamento 402/2013): clave A, pero la C («El proponente determina la significatividad del cambio.») coincide con el art. 4.1.
- **Q78** (LRJSP, art. 32.9): la A también es un supuesto del artículo, pero incompleto; se premia la cláusula completa.
- **Q128 y Q139**: redacción frágil; en Q139 se pregunta «qué autorización» y las opciones dicen si hace falta.
- **Q125** (inglés): también vale «It’s a good idea to leave now.», pero la clave es «We should leave.» (*had better* = *should*).

Lección: el tribunal copia un pasaje concreto y no siempre comprueba que otra opción también sea verdadera. **[Inferido]** Ante dos verdaderas, elige la más literal y completa; apunta el número y la duda en el cuadernillo y reclama en los 3 días hábiles tras las plantillas, citando el artículo y el texto que respalda la otra opción.
