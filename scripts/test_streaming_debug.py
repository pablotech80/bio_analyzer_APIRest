#!/usr/bin/env python3
"""
Script de debugging para probar el streaming del asistente
"""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT")

print("=" * 60)
print("TEST: Creando thread y probando streaming simple")
print("=" * 60)

try:
    # Crear thread
    thread = client.beta.threads.create()
    print(f"✅ Thread creado: {thread.id}")
    
    # Enviar mensaje
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hola, ¿cómo estás?"
    )
    print(f"✅ Mensaje enviado")
    
    # Test 1: Streaming básico sin tools
    print("\n📡 Iniciando streaming...")
    full_response = ""
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    ) as stream:
        for event in stream:
            print(f"   Event: {event.event}")
            
            if event.event == 'thread.message.delta':
                for content in event.data.delta.content:
                    if hasattr(content, 'text') and hasattr(content.text, 'value'):
                        chunk = content.text.value
                        full_response += chunk
                        print(f"   Chunk: {chunk}", end='', flush=True)
    
    print(f"\n\n✅ Respuesta completa recibida ({len(full_response)} caracteres)")
    print(f"📝 Respuesta: {full_response[:200]}...")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
