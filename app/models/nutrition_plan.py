"""
Modelo para planes nutricionales personalizados creados manualmente por el admin/entrenador.
"""
from datetime import datetime
from app import db


class NutritionPlan(db.Model):
    """
    Plan nutricional personalizado asociado a un análisis biométrico.
    
    El admin/entrenador crea estos planes manualmente para cada usuario
    basándose en sus análisis biométricos y objetivos.
    """
    __tablename__ = 'nutrition_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('biometric_analyses.id'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment="Admin/Trainer que creó el plan")
    
    # Información básica del plan
    title = db.Column(db.String(200), nullable=False, comment="Título del plan (ej: Plan Definición Marzo 2025)")
    description = db.Column(db.Text, nullable=True, comment="Descripción general del plan")
    goal = db.Column(db.String(100), nullable=True, comment="Objetivo (pérdida de grasa, ganancia muscular, etc)")
    
    # Calorías y macros
    daily_calories = db.Column(db.Integer, nullable=True, comment="Calorías diarias objetivo")
    protein_grams = db.Column(db.Integer, nullable=True, comment="Proteínas diarias (g)")
    carbs_grams = db.Column(db.Integer, nullable=True, comment="Carbohidratos diarios (g)")
    fats_grams = db.Column(db.Integer, nullable=True, comment="Grasas diarias (g)")
    
    # Comidas (JSON con estructura flexible)
    meals = db.Column(db.JSON, nullable=True, comment="Array de comidas con horarios y alimentos")
    # Ejemplo: [{"name": "Desayuno", "time": "08:00", "foods": ["Avena 80g", "Claras 4u", "Plátano 1u"]}]
    
    # Notas y recomendaciones
    notes = db.Column(db.Text, nullable=True, comment="Notas adicionales del entrenador")
    supplements = db.Column(db.Text, nullable=True, comment="Suplementación recomendada")
    
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
        return f'<NutritionPlan {self.id}: {self.title} for User {self.user_id}>'
    
    def to_dict(self):
        """Serializar a diccionario para API/templates"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_id': self.analysis_id,
            'title': self.title,
            'description': self.description,
            'goal': self.goal,
            'daily_calories': self.daily_calories,
            'protein_grams': self.protein_grams,
            'carbs_grams': self.carbs_grams,
            'fats_grams': self.fats_grams,
            'meals': self.meals,
            'notes': self.notes,
            'supplements': self.supplements,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
