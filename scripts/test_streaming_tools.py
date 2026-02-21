#!/usr/bin/env python3
"""
Script para probar el streaming con tools y diagnosticar el BadRequestError
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
print("TEST: Probando tool calls en streaming")
print("=" * 60)

try:
    thread = client.beta.threads.create()
    print(f"✅ Thread creado: {thread.id}")
    
    # Mensaje que fuerza una tool call
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Consulta mi entreno del viernes"
    )
    print(f"✅ Mensaje enviado")
    
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
                        
            elif event.event == 'thread.run.requires_action':
                print("\n   [!] Requires Action Event")
                run_id = event.data.id
                tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                
                for tool_call in tool_calls:
                    print(f"   [!] Tool call id: {tool_call.id}, name: {tool_call.function.name}")
                    
                    # Simular la respuesta de la tool
                    output = json.dumps({
                        "status": "success", 
                        "data": {
                            "training_plan": {
                                "title": "TEST PLAN",
                                "frequency": "5 days",
                                "workouts": []
                            }
                        }
                    })
                    
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output
                    })
                
                print("   [!] Submitting tool outputs...")
                try:
                    # El error BadRequestError probablemente ocurre aquí
                    stream.submit_tool_outputs(tool_outputs)
                    print("   [!] Outputs submitted successfully")
                except Exception as e:
                    print(f"\n❌ Error enviando tool outputs: {type(e).__name__}: {e}")
                    raise
    
    print(f"\n\n✅ Respuesta completa: {full_response[:100]}...")
    
except Exception as e:
    print(f"\n❌ Error general: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
