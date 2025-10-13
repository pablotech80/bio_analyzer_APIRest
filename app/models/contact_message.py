# app/models/contact_message.py
"""
Modelo para mensajes de contacto cliente-entrenador
"""
from datetime import datetime

from app import db


class ContactMessage(db.Model):
    """
    Mensajes enviados por clientes al entrenador/admin.

    Permite comunicación simple sin sistema complejo de chat.
    """

    __tablename__ = "contact_messages"

    # Identificación
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Contenido del mensaje
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Referencia opcional a análisis
    analysis_id = db.Column(
        db.Integer, db.ForeignKey("biometric_analyses.id"), nullable=True
    )

    # Estado
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = db.relationship("User", backref="messages")
    analysis = db.relationship("BiometricAnalysis", backref="messages")

    def to_dict(self):
        """Serializar a diccionario para API"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "user_email": self.user.email if self.user else None,
            "subject": self.subject,
            "message": self.message,
            "analysis_id": self.analysis_id,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def mark_as_read(self):
        """Marcar mensaje como leído"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f"<ContactMessage {self.id} from User {self.user_id}>"
