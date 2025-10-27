from datetime import datetime
from app import db

class ProgressPhoto(db.Model):
    """
    Foto de progreso subida por el usuario.
    """
    __tablename__ = 'progress_photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entry_date = db.Column(db.Date, default=datetime.utcnow)
    photo_type = db.Column(db.Enum('front', 'side', 'back', name='photo_types'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)  # Ruta o URL de la imagen
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='progress_photos')

    def __repr__(self):
        return f'<ProgressPhoto user_id={self.user_id} type={self.photo_type}>'
