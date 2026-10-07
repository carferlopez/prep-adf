# ADN del Tribunal ADIF: guía de estilo

Esta guía sale de analizar **559 preguntas reales** de temario de las convocatorias de 2022 a 2025 (Técnico y Mando Intermedio/Cuadro), 481 de ellas con la respuesta de la plantilla correctora oficial. El corpus está en `estilo/ejemplos.json` y se regenera con `scripts/extraer_examenes.py`.

## Formato del examen

- 4 opciones (a, b, c, d) y **una y solo una** correcta.
- Corrección: **Aciertos − Errores/3**. Las respuestas en blanco no puntúan.
- Conocimiento Específico: 15 preguntas + 3 de reserva (16-18), en 15 minutos.
- Conocimiento General: 15 preguntas + 3 de reserva, dentro de la Prueba Común de 45 minutos.

## Enunciado

| Rasgo | Frecuencia real |
|---|---|
| Pregunta directa con `¿…?` | 75 % |
| Frase a completar que termina en `:` | 24 % |
| Empieza citando la norma ("Según…", "Conforme a…", "De acuerdo con…", "A tenor de…", "Acorde con…") | 52 % |
| Cita el artículo concreto ("Según el artículo 143 de la Ley 47/2003…") | 8 % |
| Formulación negativa (NO, INCORRECTA, "no es") | 13 % |
| Longitud mediana | ~160 caracteres |

Fórmulas literales que repite el tribunal:

- `Según la Ley 47/2003, General Presupuestaria, ¿a quién corresponde…?`
- `Según se recoge en el Real Decreto Legislativo 2/2015, de 23 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto de los Trabajadores, ¿…?` (cita la norma con su título completo y la repite en cada pregunta)
- `Según lo dispuesto en el Real Decreto 203/2021, ¿…?`
- `¿Cuál de los siguientes … NO …?` (el **NO va en mayúsculas**)
- `Señale la afirmación INCORRECTA: Según la …`
- `¿Cuál de las siguientes afirmaciones es correcta conforme a …?`
- `NO tendrán la consideración de …, según el artículo X…:` (frase a completar negativa)

Rasgos de redacción:

- Registro formal y administrativo, con la norma identificada por número y año, y a veces también por su nombre completo.
- El enunciado **no da pistas** de la respuesta. Cuando la pregunta es larga, es porque reproduce el supuesto de hecho del artículo (umbrales, condiciones) y deja fuera solo la consecuencia.
- Dentro de una misma ley, el tribunal pregunta casi siempre por **quién** (órgano competente), **cuánto** (plazos, porcentajes, cuantías), **qué** (definiciones, clases o formas) y **a quién se aplica** (ámbito).

## Opciones

- Longitud mediana de unos 56 caracteres. Las cuatro opciones tienen **la misma estructura gramatical** y longitudes parecidas.
- La correcta es la más larga en el 34 % de los casos (por azar sería el 25 %). Hay un sesgo leve, no una regla.
- "Todas/ninguna de las anteriores" es muy raro (menos del 2 %). **No usarlo.**
- Posición de la correcta: A 28 %, B 27 %, C 26 % y D 19 %. Está bastante repartida.
- Terminan en punto cuando son frases (`a) Al Tribunal de Cuentas.`). Las numéricas son cortas (`a) A los 3 años.`).

### Tipos de distractor (por orden de frecuencia)

1. **Cifra desplazada**: la misma frase con otro número (2 %, 3 % o 6 %; 1, 2, 3 o 4 metros; 3, 2, 4 años o 1 año). La correcta suele estar en medio de la serie, no en un extremo.
2. **Órgano cambiado**: un órgano real del mismo ámbito pero sin esa competencia (IGAE frente a Tribunal de Cuentas, AIReF o SNCA; Ministro de Hacienda frente a Consejo de Ministros frente a Comisión Delegada para Asuntos Económicos; CNMC frente a Comité de Regulación Ferroviaria).
3. **Regla y excepción invertidas**: "con carácter general funcionario y excepcionalmente laboral" frente a lo contrario.
4. **Elemento ajeno en una enumeración**: en las preguntas NO, tres elementos literales de la lista legal y uno verosímil que no está, o un elemento de otra lista cercana (por ejemplo, "fiscalización de los programas de actuación presupuestaria" entre las formas de control de la IGAE).
5. **Ámbito ampliado o reducido**: "Solo a la AGE…" o "A cualquier entidad pública o privada que se financie mayoritariamente…" frente al ámbito real.
6. **Distractor de sentido común**: alguna opción claramente absurda para quien conoce la materia ("Siempre", "Nunca", "Redactar informes de producción"). Suele haber 1 por pregunta, como mucho.

## Reglas para generar preguntas al estilo del tribunal

1. Cada pregunta se apoya en un fragmento **literal** del texto oficial. La opción correcta reproduce ese texto casi palabra por palabra.
2. Los distractores son **verosímiles**: términos que aparecen en la misma norma (otros órganos, otros plazos, otras listas). No se inventan figuras inexistentes.
3. Hay que preguntar lo que el tribunal pregunta: competencias, plazos y cifras, definiciones, clasificaciones y enumeraciones, y ámbito de aplicación. No hay que preguntar por la fecha de publicación, el número de disposición o las derogaciones.
4. Mezcla aproximada: 75 % `¿…?` y 25 % frase a completar con `:`; un 15 % con formulación negativa en mayúsculas.
5. Repartir la correcta entre A, B, C y D, evitando que la correcta sea siempre la más larga.
6. En un examen de 18 preguntas no se repite el mismo artículo más de dos veces.

## Ejemplos reales de la Ley 47/2003 (Gestión 2025)

```
Según el artículo 142 de la Ley 47/2003, General Presupuestaria, ¿cuál de los siguientes NO es
una forma de control de la gestión económico-financiera a efectuar por la Intervención General
de la Administración del Estado (IGAE)?
a) El ejercicio de la función interventora.
b) El control financiero permanente.
c) La auditoría pública.
d) La fiscalización de los programas de actuación presupuestaria.        ← correcta (D)
```

```
Según la Ley 47/2003, General Presupuestaria, ¿quién eleva el anteproyecto de Ley de
Presupuestos Generales del Estado al órgano al que corresponde su tramitación?
a) La Comisión Delegada del Gobierno para Asuntos Económicos.
b) El Presidente del Gobierno.
c) El Ministro de Hacienda.                                              ← correcta (C)
d) El Consejo de Ministros.
```

```
Según la Ley 47/2003, General Presupuestaria, ¿cuál de los siguientes organismos NO forma parte
del sector público institucional estatal?
a) Los organismos públicos vinculados o dependientes de la Administración General del Estado.
b) Las autoridades administrativas independientes.
c) La Administración General del Estado.                                 ← correcta (C)
d) Las sociedades mercantiles estatales.
```
