import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user_history",
            "description": "Obtiene el historial de analisis biometricos del usuario para ver su progreso o comparar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Numero maximo de analisis a recuperar (por defecto 5)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_plans",
            "description": "Obtiene el plan de nutricion y entrenamiento actual (asociados al ultimo analisis) del usuario.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

print(f"Actualizando asistente {ASSISTANT_ID} con nuevas herramientas...")
try:
    assistant = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tools=tools,
        instructions="Eres FitMaster AI, un entrenador personal experto y nutricionista de CoachBodyFit360. Tienes acceso al historial biometrico del usuario y sus planes de dieta/entreno actuales a traves de las herramientas proporcionadas. Usalas siempre que necesites consultar el progreso, hacer comparativas o revisar el plan asignado. Responde siempre de forma profesional, concisa y motivadora basandote en DATOS REALES del usuario."
    )
    print("✅ Asistente actualizado exitosamente.")
except Exception as e:
    print(f"❌ Error actualizando asistente: {e}")
