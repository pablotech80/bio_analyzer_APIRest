import logging
import os
from datetime import datetime
from typing import Dict

from app import db
from app.models.telegram import TelegramLinkToken, UserTelegramLink
from app.models.user import User
from app.services.fitmaster_service import FitMasterService
import requests

logger = logging.getLogger(__name__)

class TelegramIntegrationService:
    """
    Servicio para manejar la lógica de integración con Telegram:
    - Validación de comandos (/link)
    - Envío de mensajes de vuelta a Telegram
    - Orquestación con FitMaster AI
    """
    
    SECRET_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_URL = f"https://api.telegram.org/bot{SECRET_TOKEN}"

    @classmethod
    def process_webhook_data(cls, data: Dict) -> None:
        """
        Punto de entrada principal para procesar datos del webhook de Telegram.
        """
        if "message" not in data:
            return

        message = data["message"]
        chat_id = message["chat"]["id"]
        telegram_user_id = message["from"]["id"]
        text = message.get("text", "")

        if text.startswith("/start"):
            cls.send_message(chat_id, "¡Hola! Soy FitMaster. Para vincular tu cuenta, usa el comando `/link TU_TOKEN` que generaste en la web.")
        
        elif text.startswith("/link"):
            cls.handle_link_command(chat_id, telegram_user_id, text)
        
        else:
            cls.handle_user_message(chat_id, telegram_user_id, text)

    @classmethod
    def handle_link_command(cls, chat_id: int, telegram_user_id: int, text: str) -> None:
        """
        Maneja el comando /link <token>
        """
        parts = text.split()
        if len(parts) < 2:
            cls.send_message(chat_id, "Formato incorrecto. Usa: `/link TU_TOKEN`")
            return

        token_str = parts[1].upper()
        
        # Buscar token válido
        token_record = TelegramLinkToken.query.filter_by(token=token_str, used_at=None).first()
        
        if not token_record or token_record.is_expired:
            cls.send_message(chat_id, "❌ Token inválido o expirado. Genera uno nuevo en la web.")
            return

        # Verificar si el telegram_user_id ya está vinculado
        existing_link = UserTelegramLink.query.filter_by(telegram_user_id=str(telegram_user_id)).first()
        if existing_link:
            cls.send_message(chat_id, "⚠️ Esta cuenta de Telegram ya está vinculada a un usuario.")
            return

        # Crear vínculo
        try:
            new_link = UserTelegramLink(
                user_id=token_record.user_id,
                telegram_user_id=str(telegram_user_id),
                telegram_chat_id=str(chat_id),
                status="verified",
                verified_at=datetime.utcnow()
            )
            token_record.used_at = datetime.utcnow()
            db.session.add(new_link)
            db.session.commit()
            
            user = User.query.get(new_link.user_id)
            cls.send_message(chat_id, f"✅ ¡Vinculación exitosa, {user.username}! Ahora puedes hacerme consultas sobre tu progreso físico y nutrición.")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al vincular Telegram: {e}")
            cls.send_message(chat_id, "❌ Error interno al procesar la vinculación.")

    @classmethod
    def handle_user_message(cls, chat_id: int, telegram_user_id: int, text: str) -> None:
        """
        Procesa mensajes normales de usuarios vinculados usando FitMaster AI.
        """
        link = UserTelegramLink.query.filter_by(telegram_user_id=str(telegram_user_id), status="verified").first()
        
        if not link:
            cls.send_message(chat_id, "⚠️ Tu cuenta no está vinculada. Usa `/link TU_TOKEN` para comenzar.")
            return

        # Notificar al usuario que estamos procesando (typing...)
        cls.send_chat_action(chat_id, "typing")

        try:
            # Obtener contexto del usuario (último análisis)
            from app.models.biometric_analysis import BiometricAnalysis
            last_analysis = BiometricAnalysis.query.filter_by(user_id=link.user_id).order_by(BiometricAnalysis.created_at.desc()).first()
            
            context = {}
            if last_analysis:
                context = last_analysis.to_dict(include_fitmaster=False)
            
            # Usar el nuevo método chat_query con memoria multi-tenant
            reply_text = FitMasterService.chat_query(text, user_id=link.user_id, context=context)
            
            cls.send_message(chat_id, reply_text)
            
        except Exception as e:
            logger.error(f"Error en handle_user_message: {e}")
            cls.send_message(chat_id, "Lo siento, FitMaster no está disponible en este momento.")

    @classmethod
    def send_message(cls, chat_id: int, text: str) -> bool:
        """Envía un mensaje de vuelta a Telegram."""
        if not cls.SECRET_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN no configurado")
            return False
            
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            r = requests.post(f"{cls.API_URL}/sendMessage", json=payload)
            r.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error enviando mensaje a Telegram: {e}")
            return False

    @classmethod
    def send_chat_action(cls, chat_id: int, action: str = "typing") -> None:
        """Envía una acción de chat (ej: 'typing') para mejorar el UX."""
        if not cls.SECRET_TOKEN:
            return
            
        payload = {"chat_id": chat_id, "action": action}
        try:
            requests.post(f"{cls.API_URL}/sendChatAction", json=payload)
        except Exception as e:
            logger.error(f"Error en chat action: {e}")
