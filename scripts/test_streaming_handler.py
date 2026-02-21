#!/usr/bin/env python3
"""
Script para probar el streaming con tools usando AssistantEventHandler
"""
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT")

print("=" * 60)
print("TEST: Probando tool calls en streaming con EventHandler")
print("=" * 60)

class EventHandler(AssistantEventHandler):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id
        self.full_response = ""

    @override
    def on_text_delta(self, delta, snapshot):
        self.full_response += delta.value
        print(f"   Chunk: {delta.value}", end='', flush=True)

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            print("\n   [!] Requires Action Event")
            run_id = event.data.id
            tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            
            for tool_call in tool_calls:
                print(f"   [!] Tool call id: {tool_call.id}, name: {tool_call.function.name}")
                
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
            self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.thread_id),
        ) as stream:
            for event in stream:
                # El stream interno procesará recursivamente los eventos
                pass

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
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        event_handler=EventHandler(thread.id),
    ) as stream:
        stream.until_done()
    
    print(f"\n\n✅ Done!")
    
except Exception as e:
    print(f"\n❌ Error general: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
