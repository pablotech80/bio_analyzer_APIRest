"""
Modelo para planes de entrenamiento personalizados creados manualmente por el admin/entrenador.
"""
from datetime import datetime
from app import db


class TrainingPlan(db.Model):
    """
    Plan de entrenamiento personalizado asociado a un análisis biométrico.
    
    El admin/entrenador crea estos planes manualmente para cada usuario
    basándose en sus análisis biométricos y objetivos.
    """
    __tablename__ = 'training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('biometric_analyses.id'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment="Admin/Trainer que creó el plan")
    
    # Información básica del plan
    title = db.Column(db.String(200), nullable=False, comment="Título del plan (ej: Rutina Hipertrofia 4 días)")
    description = db.Column(db.Text, nullable=True, comment="Descripción general del plan")
    goal = db.Column(db.String(100), nullable=True, comment="Objetivo (hipertrofia, fuerza, resistencia, etc)")
    
    # Configuración del plan
    frequency = db.Column(db.String(100), nullable=True, comment="Frecuencia semanal (ej: 4 días/semana)")
    routine_type = db.Column(db.String(100), nullable=True, comment="Tipo de rutina (PPL, Torso/Pierna, Full Body)")
    duration_weeks = db.Column(db.Integer, nullable=True, comment="Duración en semanas")
    
    # Rutina (JSON con estructura flexible)
    workouts = db.Column(db.JSON, nullable=True, comment="Array de entrenamientos por día")
    # Ejemplo: [{"day": "Lunes", "name": "Push", "exercises": [{"name": "Press banca", "sets": 4, "reps": "8-10"}]}]
    
    # Notas y recomendaciones
    notes = db.Column(db.Text, nullable=True, comment="Notas adicionales del entrenador")
    warm_up = db.Column(db.Text, nullable=True, comment="Calentamiento recomendado")
    cool_down = db.Column(db.Text, nullable=True, comment="Enfriamiento/estiramiento")
    
    # Vigencia del plan
    start_date = db.Column(db.Date, nullable=True, comment="Fecha de inicio del plan")
    end_date = db.Column(db.Date, nullable=True, comment="Fecha de fin del plan")
    is_active = db.Column(db.Boolean, default=True, comment="Plan activo o archivado")
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', foreign_keys=[user_id])
    analysis = db.relationship('BiometricAnalysis', foreign_keys=[analysis_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<TrainingPlan {self.id}: {self.title} for User {self.user_id}>'
    
    def to_dict(self):
        """Serializar a diccionario para API/templates"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_id': self.analysis_id,
            'title': self.title,
            'description': self.description,
            'goal': self.goal,
            'frequency': self.frequency,
            'routine_type': self.routine_type,
            'duration_weeks': self.duration_weeks,
            'workouts': self.workouts,
            'notes': self.notes,
            'warm_up': self.warm_up,
            'cool_down': self.cool_down,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
