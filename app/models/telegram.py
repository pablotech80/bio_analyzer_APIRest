# app/models/telegram.py
from datetime import datetime, timedelta
import secrets
from app import db


class UserTelegramLink(db.Model):
    """
    Vínculo verificado entre un usuario de la plataforma y su cuenta de Telegram.
    """
    __tablename__ = "user_telegram_links"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    telegram_user_id = db.Column(db.String(50), nullable=False, unique=True, index=True)
    telegram_chat_id = db.Column(db.String(50), nullable=True)
    openai_thread_id = db.Column(db.String(100), nullable=True)

    status = db.Column(db.Enum("pending", "verified", "revoked", name="telegram_link_status"), default="verified")

    verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación
    user = db.relationship("User", backref=db.backref("telegram_link", uselist=False, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<UserTelegramLink user_id={self.user_id} telegram_id={self.telegram_user_id}>"


class TelegramLinkToken(db.Model):
    """
    Token temporal para vincular una cuenta de Telegram (anti-suplantación).
    """
    __tablename__ = "telegram_link_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = db.Column(db.String(10), unique=True, nullable=False, index=True)

    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.token:
            # Generar un token corto alfanumérico legible de 6 caracteres
            self.token = secrets.token_hex(3).upper()
        if not self.expires_at:
            # Expira en 15 minutos por defecto
            self.expires_at = datetime.utcnow() + timedelta(minutes=15)

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self):
        return self.used_at is None and not self.is_expired

    def __repr__(self):
        return f"<TelegramLinkToken user_id={self.user_id} token={self.token}>"


class ConversationMessage(db.Model):
    """
    Historial de mensajes de la conversación en Telegram para memoria de corto/mediano plazo.
    """
    __tablename__ = "telegram_conversation_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = db.Column(db.Enum("user", "assistant", "system", name="message_role"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Para RAG futuro: almacenar el embedding si es necesario
    # vector_id = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }


class LLMUsageLedger(db.Model):
    """
    Registro de consumo de tokens por usuario para control de costes y cuotas.
    """
    __tablename__ = "llm_usage_ledger"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    model_name = db.Column(db.String(50), nullable=False)
    prompt_tokens = db.Column(db.Integer, default=0)
    completion_tokens = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)

    # Canal de origen (telegram, web, api)
    channel = db.Column(db.String(20), default="telegram")

    cost_usd = db.Column(db.Float, default=0.0)  # Coste estimado en USD

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
