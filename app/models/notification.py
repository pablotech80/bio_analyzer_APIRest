"""
Modelo de notificaciones para usuarios.
"""
from datetime import datetime
from app import db


class Notification(db.Model):
    """
    Notificaciones para usuarios sobre planes disponibles, actualizaciones, etc.
    """
    __tablename__ = "notifications"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Contenido
    title = db.Column(db.String(200), nullable=False, comment="Título de la notificación")
    message = db.Column(db.Text, nullable=False, comment="Mensaje de la notificación")
    notification_type = db.Column(
        db.String(50), 
        nullable=False, 
        default="info",
        comment="Tipo: info, success, warning, danger"
    )
    
    # Estado
    is_read = db.Column(db.Boolean, default=False, nullable=False, comment="Si fue leída")
    read_at = db.Column(db.DateTime, nullable=True, comment="Fecha de lectura")
    
    # Referencias opcionales
    nutrition_plan_id = db.Column(db.Integer, db.ForeignKey("nutrition_plans.id", ondelete="SET NULL"), nullable=True)
    training_plan_id = db.Column(db.Integer, db.ForeignKey("training_plans.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    user = db.relationship("User", backref="notifications")
    nutrition_plan = db.relationship("NutritionPlan", backref="notifications")
    training_plan = db.relationship("TrainingPlan", backref="notifications")
    
    def __repr__(self):
        return f"<Notification {self.id}: {self.title} for User {self.user_id}>"
    
    def mark_as_read(self):
        """Marcar notificación como leída"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convertir a diccionario para API"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'nutrition_plan_id': self.nutrition_plan_id,
            'training_plan_id': self.training_plan_id,
            'created_at': self.created_at.isoformat()
        }
