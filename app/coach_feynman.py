import sqlite3
from google import genai
from motor_adaptativo import get_db_connection

def generar_diagnostico_feynman(api_key: str) -> str:
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get total answers to know if we have enough data
    cur.execute("SELECT COUNT(*) FROM historial_respuestas")
    total_respuestas = cur.fetchone()[0]
    
    if total_respuestas < 10:
        conn.close()
        return "Aún no tienes suficientes respuestas registradas (mínimo 10) para que pueda analizar tus patrones de fallo. ¡Sigue practicando un poco más!"

    # Get the worst performing articles
    cur.execute("""
        SELECT documento, titulo_unidad, contenido_literal, fallos_totales, ultimo_error_tipo
        FROM unidades_temario
        WHERE fallos_totales > 0
        ORDER BY fallos_totales DESC, dominio_score ASC
        LIMIT 15
    """)
    peores = cur.fetchall()
    conn.close()

    if not peores:
        return "¡Enhorabuena! No tienes fallos registrados. Sigue haciendo tests para que pueda identificar tus puntos ciegos."

    prompt_context = "Aquí tienes los preceptos del temario (legislación ferroviaria, contratos, sector público, etc.) en los que más está fallando el opositor:\n\n"
    for row in peores:
        prompt_context += f"--- Documento: {row['documento']} ---\n"
        prompt_context += f"Artículo: {row['titulo_unidad']}\n"
        prompt_context += f"Veces fallado: {row['fallos_totales']}\n"
        prompt_context += f"Patrón de error: {row['ultimo_error_tipo'] or 'No especificado'}\n"
        prompt_context += f"Texto del artículo: {row['contenido_literal']}\n\n"

    system_prompt = """Eres Richard Feynman, pero actuando como el 'Coach de Oposiciones' definitivo. Eres directo, cercano, y tienes una capacidad legendaria para explicar cosas aburridas o complejas de la forma más intuitiva posible. Vas al "quid de la cuestión".

Tu objetivo es analizar los datos de fallos del opositor y devolver un reporte en formato Markdown. 
REGLA DE ORO (CERO ALUCINACIONES): Basa tus explicaciones ESTRICTAMENTE en el "Texto del artículo" proporcionado. No inventes plazos, no asumas competencias que no estén en el texto, y si el texto no detalla algo, no lo inventes de tu conocimiento previo.

ESTRUCTURA OBLIGATORIA DEL REPORTE:

### 🔍 1. Patrones de Fallo
Analiza la lista de artículos fallados y busca el patrón común. ¿Le cuestan los plazos? ¿Confunde competencias de distintos órganos (ej. Consejo de Administración vs Presidente)? ¿Falla en definiciones clave? Sé específico y dile exactamente dónde está resbalando.

### 🧠 2. La Explicación Feynman (Al grano)
Elige los 2 o 3 conceptos más repetidos en sus fallos y explícaselos usando la técnica Feynman: lenguaje de la calle, analogías simples y yendo al núcleo del porqué la norma es así, para que no tenga que memorizar a lo bruto, sino comprender la lógica.

### 🎧 3. Tu Guion para Google NotebookLM
Redacta aquí un texto en primera persona, claro y estructurado, pensado EXCLUSIVAMENTE para que el opositor lo copie y lo pegue en Google NotebookLM para generar un "Audio Overview" (podcast a dos voces). 
El texto debe ser un resumen de los conceptos que más falla, escrito como si fuera un apunte de repaso. 
Ejemplo de inicio: "Este es un documento de repaso sobre las competencias del Consejo de Administración de ADIF frente a las del Ministerio. Hay que tener claro que el Consejo hace X, pero el Ministerio aprueba Y..." (Asegúrate de incluir la información real de los artículos fallados).
"""

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_context,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.4
            )
        )
        return response.text
    except Exception as e:
        try:
            response_fb = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt_context,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.4
                )
            )
            return response_fb.text
        except Exception as e2:
            return f"Error al contactar con Gemini AI para generar el diagnóstico. Detalle: {str(e2)}"

if __name__ == '__main__':
    pass
