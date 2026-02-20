import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PRODUCTION_URL = "https://app.coachbodyfit360.com" # O el dominio que uses en producción
WEBHOOK_URL = f"{PRODUCTION_URL}/integrations/telegram/webhook"
API_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"

if not TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado en el archivo .env")
    exit(1)

print(f"📡 Configurando el webhook oficial de Telegram a: {WEBHOOK_URL} ...")
response = requests.post(API_URL, json={"url": WEBHOOK_URL})

if response.status_code == 200:
    print("✅ Webhook configurado exitosamente!")
    print(response.json())
else:
    print("❌ Error al configurar el webhook:")
    print(response.text)
