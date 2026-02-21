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
            cls.send_message(chat_id, "¡Hola! Soy FitMaster. Para vincular tu cuenta, usa el comando `/link TU_TOKEN` que generaste en la web. Si ya estás vinculado y quieres reiniciar la conversación, usa `/reset`.")
        
        elif text.startswith("/link"):
            cls.handle_link_command(chat_id, telegram_user_id, text)
            
        elif text.startswith("/reset"):
            cls.handle_reset_command(chat_id, telegram_user_id)
        
        else:
            cls.handle_user_message(chat_id, telegram_user_id, text)

    @classmethod
    def handle_reset_command(cls, chat_id: int, telegram_user_id: int) -> None:
        """
        Borra el thread_id actual para forzar al agente a crear una nueva conversación limpia.
        """
        link = UserTelegramLink.query.filter_by(telegram_user_id=str(telegram_user_id), status="verified").first()
        if not link:
            cls.send_message(chat_id, "⚠️ Tu cuenta no está vinculada.")
            return
            
        try:
            # Borrar el thread_id forzará la creación de uno nuevo en el próximo mensaje
            old_thread = link.openai_thread_id
            link.openai_thread_id = None
            db.session.commit()
            
            logger.info(f"Thread reseteado para usuario {link.user_id} (viejo: {old_thread})")
            cls.send_message(chat_id, "🔄 Memoria de la conversación reiniciada. ¿En qué te puedo ayudar ahora con tu progreso o plan?")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error reseteando thread: {e}")
            cls.send_message(chat_id, "❌ Error al intentar reiniciar la conversación.")

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
                # Ocultar intencionalmente fitmaster_data del contexto para evitar que el agente lea planes viejos/sugeridos
                context = last_analysis.to_dict(include_fitmaster=False)
                # Asegurar que fitmaster_data no esté presente incluso si to_dict falló en excluirlo
                if 'fitmaster_data' in context:
                    del context['fitmaster_data']
            
            # Variables para streaming
            message_id = None
            accumulated_text = ""
            last_update_length = 0
            
            def stream_callback(chunk: str):
                """Callback para enviar chunks en tiempo real a Telegram."""
                nonlocal message_id, accumulated_text, last_update_length
                
                try:
                    accumulated_text += chunk
                    
                    # Enviar/actualizar mensaje cada 100 caracteres (evitar rate limit)
                    chars_since_update = len(accumulated_text) - last_update_length
                    
                    if chars_since_update >= 100:
                        if message_id:
                            # Actualizar mensaje existente
                            success = cls.edit_message(chat_id, message_id, accumulated_text)
                            if success:
                                last_update_length = len(accumulated_text)
                        else:
                            # Enviar primer mensaje (esperar al menos 50 caracteres)
                            if len(accumulated_text) >= 50:
                                msg_id = cls.send_message_get_id(chat_id, accumulated_text)
                                if msg_id:
                                    message_id = msg_id
                                    last_update_length = len(accumulated_text)
                except Exception as e:
                    logger.error(f"Error en stream_callback: {e}")
                    # No re-lanzar la excepción para no romper el stream
            
            # Usar chat_query con streaming
            reply_text = FitMasterService.chat_query(
                text, 
                user_id=link.user_id, 
                context=context,
                stream_callback=stream_callback
            )
            
            # Enviar mensaje final si no se envió nada por streaming
            if not message_id:
                cls.send_message(chat_id, reply_text)
            elif accumulated_text != reply_text:
                # Actualizar con el texto final limpio
                cls.edit_message(chat_id, message_id, reply_text)
            
        except Exception as e:
            logger.error(f"Error en handle_user_message: {type(e).__name__}: {e}", exc_info=True)
            cls.send_message(chat_id, f"Lo siento, FitMaster no está disponible en este momento. ({type(e).__name__})")

    @staticmethod
    def _md_to_telegram_html(text: str) -> str:
        """Convierte Markdown del Assistants API a HTML compatible con Telegram."""
        import re

        # Headers → Bold
        text = re.sub(r'^#{1,6}\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

        # Bold: **text** → <b>text</b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

        # Italic: *text* → <i>text</i> (but not bullet points)
        text = re.sub(r'(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<i>\1</i>', text)

        # Inline code: `text` → <code>text</code>
        text = re.sub(r'`([^`]+?)`', r'<code>\1</code>', text)

        # Code blocks: ```text``` → <pre>text</pre>
        text = re.sub(r'```(?:\w+)?\n?(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)

        # Bullet points: - item → • item
        text = re.sub(r'^[-*]\s+', '• ', text, flags=re.MULTILINE)

        # Escape remaining HTML special chars that aren't part of our tags
        # (Telegram requires this for HTML mode)
        # We do this carefully to not break our own tags
        def escape_outside_tags(t):
            parts = re.split(r'(<[^>]+>)', t)
            for i, part in enumerate(parts):
                if not part.startswith('<'):
                    part = part.replace('&', '&amp;')
                    part = part.replace('<', '&lt;')
                    part = part.replace('>', '&gt;')
                    parts[i] = part
            return ''.join(parts)

        # Don't escape — our tags are already in place
        return text

    @classmethod
    def send_message(cls, chat_id: int, text: str, use_html: bool = True) -> bool:
        """Envía un mensaje de vuelta a Telegram."""
        if not cls.SECRET_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN no configurado")
            return False

        if use_html:
            text = cls._md_to_telegram_html(text)

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML" if use_html else "Markdown"
        }
        try:
            r = requests.post(f"{cls.API_URL}/sendMessage", json=payload)
            if r.status_code != 200:
                # Fallback: enviar sin formato si HTML falla
                logger.warning(f"HTML send failed ({r.status_code}), retrying plain")
                payload["parse_mode"] = None
                payload["text"] = text
                r = requests.post(f"{cls.API_URL}/sendMessage", json=payload)
            r.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error enviando mensaje a Telegram: {e}")
            return False

    @classmethod
    def send_message_get_id(cls, chat_id: int, text: str, use_html: bool = True) -> int:
        """Envía un mensaje y devuelve el message_id para poder editarlo después."""
        if not cls.SECRET_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN no configurado")
            return None

        if use_html:
            text = cls._md_to_telegram_html(text)

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML" if use_html else None
        }
        try:
            r = requests.post(f"{cls.API_URL}/sendMessage", json=payload)
            if r.status_code == 200:
                return r.json().get("result", {}).get("message_id")
            else:
                logger.warning(f"Failed to send message: {r.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error enviando mensaje a Telegram: {e}")
            return None

    @classmethod
    def edit_message(cls, chat_id: int, message_id: int, text: str, use_html: bool = True) -> bool:
        """Edita un mensaje existente (útil para streaming)."""
        if not cls.SECRET_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN no configurado")
            return False

        if use_html:
            text = cls._md_to_telegram_html(text)

        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML" if use_html else None
        }
        try:
            r = requests.post(f"{cls.API_URL}/editMessageText", json=payload)
            r.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error editando mensaje en Telegram: {e}")
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
