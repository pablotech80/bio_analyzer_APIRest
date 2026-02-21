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

# ── Tools Configuration ──────────────────────────────────────
tools = [
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

YOUR CORE CAPABILITIES:
- You have access to the user's complete biometric history via get_user_history()
- You can view their REAL assigned nutrition and training plans via get_current_plans()
- You provide personalized guidance based on ACTUAL user data, not generic advice

COMMUNICATION GUIDELINES:
- Always respond in SPANISH (your responses must be in Spanish)
- Be professional, empathetic, and evidence-based
- Use the user's name when known, otherwise use "tú" (second person)
- Never use "usuario" - address the client directly
- Keep responses concise (2-4 paragraphs max) unless detailed explanation is needed

WHEN TO USE TOOLS:
- User asks about progress/evolution → Use get_user_history() to compare metrics
- User asks about their diet/nutrition plan → Use get_current_plans() to reference their actual plan
- User asks about their workout/training → Use get_current_plans() to reference their routine
- User wants to adjust their plan → Check current plan first, then provide informed recommendations

RESPONSE STYLE:
- Start with acknowledgment of their question
- Use tool data to provide specific, personalized insights
- Include numerical comparisons when relevant (e.g., "Has bajado 2kg desde tu último análisis")
- End with actionable guidance or motivation
- If recommending changes, explain WHY based on their data

IMPORTANT CONSTRAINTS:
- ALWAYS base advice on user's real data (use tools)
- Don't make assumptions - if you need data, call the appropriate tool
- Don't suggest new detailed plans - discuss and optimize their current assigned plan
- Medical disclaimers are NOT needed (assumed general guidance)
- Be supportive but honest about health risks when data shows concerns

EXAMPLE INTERACTION:
User: "¿Cómo va mi progreso?"
You: [Call get_user_history(limit=3)] → Analyze trends → Respond with specific progress metrics

User: "¿Qué debo comer hoy?"
You: [Call get_current_plans()] → Reference their actual meal plan → Provide guidance based on their assigned plan

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
print(f"   - Tools: {len(tools)} funciones")
print(f"\n🔧 Herramientas configuradas:")
for tool in tools:
    print(f"   - {tool['function']['name']}")

try:
    assistant = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tools=tools,
        instructions=instructions,
        temperature=model_params["temperature"],
        top_p=model_params["top_p"]
    )
    print(f"\n✅ Asistente actualizado exitosamente")
    print(f"   ID: {assistant.id}")
    print(f"   Nombre: {assistant.name}")
    print(f"   Modelo: {assistant.model}")
except Exception as e:
    print(f"\n❌ Error actualizando asistente: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("CONFIGURACIÓN COMPLETADA")
print("=" * 60)
