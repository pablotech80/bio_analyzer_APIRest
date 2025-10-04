"""SQLAlchemy model for storing biometric analyses linked to users."""
from datetime import datetime

from app import db


class BiometricAnalysis(db.Model):
    """Historical biometric analysis snapshot for a user."""

    __tablename__ = "biometric_analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # Input data
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # 'h' o 'm'
    neck = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float)

    activity_factor = db.Column(db.Float)
    activity_level = db.Column(db.String(32))
    goal = db.Column(db.String(32))

    # Calculated metrics
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)  # Tasa metabólica basal (TMB)
    tdee = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    lean_mass = db.Column(db.Float)
    fat_mass = db.Column(db.Float)
    ffmi = db.Column(db.Float)
    body_water = db.Column(db.Float)
    waist_hip_ratio = db.Column(db.Float)
    waist_height_ratio = db.Column(db.Float)
    metabolic_age = db.Column(db.Float)
    maintenance_calories = db.Column(db.Float)
    protein_grams = db.Column(db.Float)
    carbs_grams = db.Column(db.Float)
    fats_grams = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship("User", back_populates="biometric_analyses")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<BiometricAnalysis id={self.id} user_id={self.user_id} created_at={self.created_at}>"
