#!/usr/bin/env python3
"""
Test de la nueva implementación de streaming con tool calls usando _process_stream recursivo.
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
print("TEST: Nueva implementación _process_stream con tool calls")
print("=" * 60)

full_response_container = {"text": ""}

def _execute_tools(tool_calls, thread_id):
    tool_outputs = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        print(f"\n   [TOOL] Ejecutando: {function_name}")
        output = json.dumps({
            "status": "success",
            "data": {
                "training_plan": {
                    "title": "Powerbuilding TEST",
                    "frequency": "5 días",
                    "workouts": [{"day": "Viernes", "name": "Piernas", "exercises": [{"name": "Sentadilla", "sets": 5, "reps": "5"}]}]
                }
            }
        })
        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
    return tool_outputs

def _process_stream(stream_obj, thread_id):
    for event in stream_obj:
        if event.event == 'thread.message.delta':
            for content in event.data.delta.content:
                if hasattr(content, 'text') and hasattr(content.text, 'value'):
                    chunk = content.text.value
                    full_response_container["text"] += chunk
                    print(chunk, end='', flush=True)

        elif event.event == 'thread.run.requires_action':
            run_id = event.data.id
            tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
            tool_outputs = _execute_tools(tool_calls, thread_id)

            print(f"\n   [STREAM] Abriendo sub-stream para tool outputs...")
            with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs,
            ) as tool_stream:
                _process_stream(tool_stream, thread_id)

try:
    thread = client.beta.threads.create()
    print(f"✅ Thread: {thread.id}")

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Consulta mi entreno del viernes"
    )
    print("✅ Mensaje enviado\n📡 Streaming...\n")

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    ) as stream:
        _process_stream(stream, thread.id)

    print(f"\n\n✅ Respuesta completa ({len(full_response_container['text'])} chars)")
    print(f"📝 {full_response_container['text'][:200]}...")

except Exception as e:
    import traceback
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
