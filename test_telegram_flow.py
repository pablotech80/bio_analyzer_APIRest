import sys
import os
from datetime import datetime

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from app.models.user import User
from app.models.telegram import TelegramLinkToken, UserTelegramLink, ConversationMessage, LLMUsageLedger
from app.services.telegram_service import TelegramIntegrationService

def test_telegram_integration():
    app = create_app()
    with app.app_context():
        # Asegurar que las tablas existen (especialmente las nuevas de Telegram)
        db.create_all()
        print("🚀 Iniciando Test de Integración de Telegram...")

        # 1. Buscar o crear un usuario de prueba
        user = User.query.filter_by(email="test@example.com").first()
        if not user:
            print("👤 Creando usuario de prueba...")
            user = User(username="testuser", email="test@example.com")
            user.password = "password123"
            db.session.add(user)
            db.session.commit()
        
        # 2. Generar un token de vinculación
        print(f"🔑 Generando token para {user.username}...")
        token_record = TelegramLinkToken(user_id=user.id)
        db.session.add(token_record)
        db.session.commit()
        token_str = token_record.token
        print(f"✅ Token generado: {token_str}")

        # 3. Simular comando /link desde Telegram
        chat_id = 999999
        telegram_user_id = 123456
        print(f"🤖 Simulando comando: /link {token_str}")
        
        # Limpiar vínculos previos si existen
        UserTelegramLink.query.filter_by(telegram_user_id=str(telegram_user_id)).delete()
        db.session.commit()

        TelegramIntegrationService.handle_link_command(chat_id, telegram_user_id, f"/link {token_str}")
        
        # Verificar vínculo
        link = UserTelegramLink.query.filter_by(telegram_user_id=str(telegram_user_id)).first()
        if link and link.user_id == user.id:
            print("✅ Vinculación EXITOSA en Base de Datos")
        else:
            print("❌ FALLÓ la vinculación en Base de Datos")
            return

        # 4. Simular mensaje de usuario
        query_text = "Hola FitMaster, ¿cómo puedo mejorar mi masa muscular?"
        print(f"💬 Simulando mensaje: '{query_text}'")
        
        # Nota: Esto llamará a la API real de OpenAI si la KEY está configurada
        try:
            TelegramIntegrationService.handle_user_message(chat_id, telegram_user_id, query_text)
            print("✅ Procesamiento de mensaje completado")
            
            # 5. Verificar registros
            # Verificar mensajes en la conversación
            msgs = ConversationMessage.query.filter_by(user_id=user.id).all()
            print(f"📝 Mensajes guardados en historial: {len(msgs)}")
            for m in msgs:
                print(f"   - {m.role}: {m.content[:50]}...")

            # Verificar consumo de tokens
            usage = LLMUsageLedger.query.filter_by(user_id=user.id).first()
            if usage:
                print(f"💰 Registro de consumo ENCONTRADO: {usage.total_tokens} tokens (${usage.cost_usd})")
            else:
                print("⚠️ No se encontró registro de consumo (¿OpenAI falló o no está configurado?)")

        except Exception as e:
            print(f"❌ Error durante el procesamiento del mensaje: {e}")

        print("\n" + "="*40)
        print("🏁 Test finalizado")
        print("="*40)

if __name__ == "__main__":
    test_telegram_integration()
