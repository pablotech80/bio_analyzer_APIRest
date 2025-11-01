"""
Modelo para archivos multimedia del blog
"""
from datetime import datetime
from app import db


class MediaFile(db.Model):
    """Modelo para gestionar archivos multimedia (imágenes, videos, audios)"""
    
    __tablename__ = 'media_files'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información del archivo
    filename = db.Column(db.String(255), nullable=False)  # Nombre original
    file_path = db.Column(db.String(500), nullable=False, unique=True)  # Ruta en servidor
    file_url = db.Column(db.String(500), nullable=False)  # URL pública
    file_type = db.Column(db.String(50), nullable=False)  # image, video, audio
    mime_type = db.Column(db.String(100))  # image/jpeg, video/mp4, audio/mpeg
    file_size = db.Column(db.Integer)  # Tamaño en bytes
    
    # Metadata
    title = db.Column(db.String(200))  # Título descriptivo
    alt_text = db.Column(db.String(200))  # Texto alternativo (SEO)
    caption = db.Column(db.String(500))  # Descripción/caption
    
    # Dimensiones (para imágenes/videos)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    
    # Duración (para videos/audios)
    duration = db.Column(db.Integer)  # Duración en segundos
    
    # Autor
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploader = db.relationship('User', backref='media_files')
    
    # Uso
    usage_count = db.Column(db.Integer, default=0)  # Cuántas veces se usa
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<MediaFile {self.filename}>'
    
    def to_dict(self):
        """Convierte el archivo a diccionario para JSON"""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_url': self.file_url,
            'file_type': self.file_type,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'title': self.title,
            'alt_text': self.alt_text,
            'caption': self.caption,
            'width': self.width,
            'height': self.height,
            'duration': self.duration,
            'uploaded_by': self.uploaded_by,
            'usage_count': self.usage_count,
            'uploaded_at': self.uploaded_at.isoformat()
        }
    
    @property
    def file_size_human(self):
        """Retorna el tamaño del archivo en formato legible"""
        if not self.file_size:
            return 'N/A'
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    @property
    def is_image(self):
        """Verifica si es una imagen"""
        return self.file_type == 'image'
    
    @property
    def is_video(self):
        """Verifica si es un video"""
        return self.file_type == 'video'
    
    @property
    def is_audio(self):
        """Verifica si es un audio"""
        return self.file_type == 'audio'
    
    @property
    def markdown_embed(self):
        """Genera código Markdown para insertar en posts"""
        if self.is_image:
            alt = self.alt_text or self.title or self.filename
            return f"![{alt}]({self.file_url})"
        elif self.is_video:
            title = self.title or "Video"
            return f"![video:{title}]({self.file_url})"
        elif self.is_audio:
            title = self.title or "Audio"
            return f"![audio:{title}]({self.file_url})"
        return f"[{self.filename}]({self.file_url})"
