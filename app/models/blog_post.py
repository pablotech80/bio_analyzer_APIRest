"""
Modelo para posts del blog
"""
from datetime import datetime
from app import db


class BlogPost(db.Model):
    """Modelo para posts del blog"""
    
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Contenido
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.String(300))  # Resumen corto para listados
    content = db.Column(db.Text, nullable=False)  # Markdown
    featured_image = db.Column(db.String(500))  # URL de la imagen destacada
    
    # Categorización
    category = db.Column(db.String(50), index=True)  # Entrenamiento, Nutrición, etc
    tags = db.Column(db.String(200))  # Separados por comas
    
    # SEO
    meta_description = db.Column(db.String(160))  # Para meta tags
    meta_keywords = db.Column(db.String(200))  # Keywords separadas por comas
    
    # Autor
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='blog_posts')
    
    # Estado
    is_published = db.Column(db.Boolean, default=False)  # Draft vs Publicado
    published_at = db.Column(db.DateTime, index=True)  # Fecha de publicación
    
    # Métricas
    views_count = db.Column(db.Integer, default=0)
    reading_time = db.Column(db.Integer)  # Minutos estimados de lectura
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    def to_dict(self):
        """Convierte el post a diccionario para JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'content': self.content,
            'featured_image': self.featured_image,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'meta_description': self.meta_description,
            'meta_keywords': self.meta_keywords.split(',') if self.meta_keywords else [],
            'author': {
                'id': self.author.id,
                'name': self.author.full_name,
                'email': self.author.email
            } if self.author else None,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'views_count': self.views_count,
            'reading_time': self.reading_time,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @property
    def tags_list(self):
        """Retorna tags como lista"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()] if self.tags else []
    
    @property
    def keywords_list(self):
        """Retorna keywords como lista"""
        return [kw.strip() for kw in self.meta_keywords.split(',') if kw.strip()] if self.meta_keywords else []
