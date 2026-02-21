#!/usr/bin/env python3
"""
Verificar la configuración actual del asistente en OpenAI
"""
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT")

print("=" * 60)
print(f"VERIFICANDO ASISTENTE: {ASSISTANT_ID}")
print("=" * 60)

try:
    assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
    
    print(f"\n📋 Información del Asistente:")
    print(f"   ID: {assistant.id}")
    print(f"   Nombre: {assistant.name}")
    print(f"   Modelo: {assistant.model}")
    print(f"   Temperatura: {assistant.temperature}")
    print(f"   Top P: {assistant.top_p}")
    
    print(f"\n🔧 Herramientas Configuradas ({len(assistant.tools)}):")
    for i, tool in enumerate(assistant.tools, 1):
        print(f"\n   {i}. {tool.type.upper()}")
        if tool.type == "function":
            print(f"      Nombre: {tool.function.name}")
            print(f"      Descripción: {tool.function.description[:100]}...")
    
    print(f"\n📝 Instrucciones del Sistema:")
    print("=" * 60)
    print(assistant.instructions[:500])
    print("\n... (truncado)")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    sys.exit(1)
