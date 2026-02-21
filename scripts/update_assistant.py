#!/usr/bin/env python3
"""
Script para actualizar el asistente FitMaster en OpenAI con:
- Instrucciones mejoradas del sistema
- Herramientas (tools) para acceso a datos del usuario
- Parámetros óptimos de modelo (temperatura, top_p)
"""
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT")
VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID", "vs_696e590964f081919aea03c44e93de54")

# ── Tools Configuration ──────────────────────────────────────
tools = [
    {
        "type": "file_search"
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_history",
            "description": "Retrieves the user's biometric analysis history to track progress and compare metrics over time. Use this when the user asks about their progress, evolution, or wants to compare current vs past results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of analyses to retrieve (default: 5, max: 10)",
                        "default": 5
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_plans",
            "description": "Retrieves the user's ACTIVE nutrition and training plans assigned by their coach/trainer. Use this when discussing diet, meals, workouts, or exercises to reference their actual assigned plan.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# ── System Instructions ──────────────────────────────────────
instructions = """
You are FitMaster AI, an expert virtual personal trainer and nutritionist for CoachBodyFit360.

CRITICAL RULE - READ CAREFULLY:
⚠️ NEVER INVENT OR ASSUME PLAN DETAILS ⚠️
- The user has REAL assigned plans in the database
- You MUST call get_current_plans() BEFORE answering ANY question about:
  • Training routines, workouts, exercises, gym days
  • Nutrition plans, meals, diet, calories, macros
  • "What should I eat/train today?"
  • "Show me my plan"
  • "What's my routine?"
- DO NOT use generic examples like "Push/Pull/Legs" or "sample meal plans"
- DO NOT reference suggested plans from biometric analysis
- ONLY use the ACTUAL plan data returned by get_current_plans()

YOUR CORE CAPABILITIES:
- You have access to the user's complete biometric history via get_user_history()
- You can view their REAL assigned nutrition and training plans via get_current_plans()
- You have a knowledge base (file_search) with expert protocols and frameworks:
  • Nutrition Hard Gate (boundaries and safety limits)
  • Nutrition Boundaries & Habits (behavioral frameworks)
  • Training Systems Knowledge (periodization, programming)
  • Readaptation Protocols (injury recovery, return to training)
  • FitMaster Behavioral Framework and Safety Guardrails
- You provide personalized guidance based on ACTUAL user data, not generic advice

COMMUNICATION GUIDELINES:
- Always respond in SPANISH (your responses must be in Spanish)
- Be professional, empathetic, and evidence-based
- Use the user's name when known, otherwise use "tú" (second person)
- Never use "usuario" - address the client directly
- Keep responses concise (2-4 paragraphs max) unless detailed explanation is needed

MANDATORY TOOL USAGE (YOU MUST FOLLOW THIS):
1. User mentions "entreno", "rutina", "ejercicio", "gimnasio", "workout" → CALL get_current_plans() FIRST
2. User mentions "dieta", "comida", "nutrición", "plan nutricional" → CALL get_current_plans() FIRST
3. User asks "¿Cómo va mi progreso?" → CALL get_user_history()
4. User wants to compare analyses → CALL get_user_history(limit=3)
5. User asks about Friday workout → CALL get_current_plans(), then check the actual training days
6. User asks technical questions (periodization, injury recovery, nutrient timing) → USE file_search to consult knowledge base
7. Use knowledge base to validate safety boundaries (e.g., extreme deficits, contraindicated exercises)

RESPONSE PROTOCOL:
1. Identify if question relates to plans or history
2. CALL the appropriate tool (get_current_plans or get_user_history)
3. WAIT for tool response
4. Use ONLY the data from tool response
5. If tool returns no data, inform user they don't have an assigned plan yet
6. NEVER make up plan details

EXAMPLE CORRECT INTERACTION:
User: "Consulta mi entreno del viernes"
You: [MUST call get_current_plans()] 
→ Receive: {"training_plan": {"title": "Powerbuilding", "frequency": 5, "workouts": [...]}}
→ Respond: "Revisando tu plan de entrenamiento Powerbuilding (5 días)..."

EXAMPLE WRONG INTERACTION:
User: "Consulta mi entreno del viernes"
You: "Aquí está una sugerencia de ejercicios para piernas..." ❌ NEVER DO THIS

IMPORTANT CONSTRAINTS:
- ALWAYS base advice on user's real data (use tools)
- Don't make assumptions - if you need data, call the appropriate tool
- Don't suggest new detailed plans - discuss and optimize their current assigned plan
- Medical disclaimers are NOT needed (assumed general guidance)
- Be supportive but honest about health risks when data shows concerns

Remember: You are a knowledgeable coach with access to the user's complete fitness journey. Use that data to provide truly personalized guidance.
"""

# ── Model Parameters ──────────────────────────────────────────
# Temperature: 0.7 (balanced creativity and consistency)
# Top_p: 1.0 (standard, full diversity - don't restrict to 0.3)
model_params = {
    "temperature": 0.7,
    "top_p": 1.0
}

print("=" * 60)
print(f"ACTUALIZANDO ASISTENTE: {ASSISTANT_ID}")
print("=" * 60)
print(f"\n📋 Configuración:")
print(f"   - Modelo: gpt-4o-mini")
print(f"   - Temperatura: {model_params['temperature']}")
print(f"   - Top P: {model_params['top_p']}")
print(f"   - Tools: {len(tools)} herramientas")
print(f"   - Vector Store: {VECTOR_STORE_ID}")
print(f"\n🔧 Herramientas configuradas:")
for tool in tools:
    if tool["type"] == "file_search":
        print(f"   - file_search (RAG con base de conocimiento)")
    else:
        print(f"   - {tool['function']['name']}")

try:
    assistant = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tools=tools,
        instructions=instructions,
        temperature=model_params["temperature"],
        top_p=model_params["top_p"],
        tool_resources={
            "file_search": {
                "vector_store_ids": [VECTOR_STORE_ID]
            }
        }
    )
    print(f"\n✅ Asistente actualizado exitosamente")
    print(f"   ID: {assistant.id}")
    print(f"   Nombre: {assistant.name}")
    print(f"   Modelo: {assistant.model}")
    print(f"   Vector Store asociado: {VECTOR_STORE_ID}")
except Exception as e:
    print(f"\n❌ Error actualizando asistente: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("CONFIGURACIÓN COMPLETADA")
print("=" * 60)
