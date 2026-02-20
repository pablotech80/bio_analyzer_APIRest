import os
import time
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = "http://localhost:5000/integrations/telegram/webhook" # Simulamos el webhook localmente

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    try:
        r = requests.get(url)
        return r.json()
    except Exception as e:
        print(f"Error obteniendo actualizaciones: {e}")
        return None

def send_to_webhook(data):
    try:
        r = requests.post(WEBHOOK_URL, json=data)
        return r.status_code
    except Exception as e:
        print(f"Error enviando al webhook local: {e}")
        return None

def run_polling():
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN no encontrado en .env")
        return

    print(f"🤖 Bot Polling iniciado para el token: {TOKEN[:10]}...")
    print(f"📡 Redirigiendo mensajes a: {WEBHOOK_URL}")
    print("Presiona Ctrl+C para detener.")

    # Eliminar webhook si existe para permitir long polling
    requests.get(f"{BASE_URL}/deleteWebhook")

    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates and updates.get("ok"):
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                print(f"📩 Nuevo mensaje de {update.get('message', {}).get('from', {}).get('first_name')}")
                status = send_to_webhook(update)
                if status == 200:
                    print("✅ Procesado correctamente por la App")
                else:
                    print(f"⚠️ Error en la App (Status: {status}). ¿Está Flask corriendo?")
        
        time.sleep(1)

if __name__ == "__main__":
    run_polling()
