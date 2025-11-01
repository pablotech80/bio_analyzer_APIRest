"""
Formularios para el blog
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Optional, URL


class BlogPostForm(FlaskForm):
    """Formulario para crear/editar posts del blog"""
    
    # Contenido principal
    title = StringField(
        'Título',
        validators=[DataRequired(message='El título es obligatorio'), Length(max=200)],
        render_kw={'placeholder': 'Ej: Guía Completa de Proteínas para Ganar Músculo'}
    )
    
    excerpt = TextAreaField(
        'Resumen (Excerpt)',
        validators=[Optional(), Length(max=300)],
        render_kw={
            'placeholder': 'Resumen corto que aparecerá en el listado de posts (máx 300 caracteres)',
            'rows': 3,
            'maxlength': '300',
            'oninput': 'updateCharCount(this, "excerpt-count", 300)'
        }
    )
    
    content = TextAreaField(
        'Contenido (Markdown)',
        validators=[DataRequired(message='El contenido es obligatorio')],
        render_kw={
            'placeholder': '# Título Principal\n\n## Subtítulo\n\nTu contenido aquí...',
            'rows': 20,
            'class': 'font-monospace',
            'style': 'white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word;'
        }
    )
    
    # Imagen destacada
    featured_image = StringField(
        'Imagen Destacada (opcional)',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'URL de imagen o deja vacío'}
    )
    
    # Categorización
    category = SelectField(
        'Categoría',
        choices=[
            ('', '-- Seleccionar Categoría --'),
            ('entrenamiento', 'Entrenamiento'),
            ('nutricion', 'Nutrición'),
            ('transformaciones', 'Transformaciones'),
            ('ciencia', 'Ciencia del Fitness'),
            ('consejos', 'Consejos y Tips'),
        ],
        validators=[DataRequired(message='Selecciona una categoría')]
    )
    
    tags = StringField(
        'Tags',
        validators=[Optional(), Length(max=200)],
        render_kw={
            'placeholder': 'proteinas, musculo, nutricion (separados por comas)',
            'maxlength': '200',
            'oninput': 'updateCharCount(this, "tags-count", 200)'
        }
    )
    
    # SEO
    meta_description = TextAreaField(
        'Meta Description (SEO)',
        validators=[Optional(), Length(max=160)],
        render_kw={
            'placeholder': 'Descripción para Google (máx 160 caracteres)',
            'rows': 2,
            'maxlength': '160',
            'oninput': 'updateCharCount(this, "meta-desc-count", 160)'
        }
    )
    
    meta_keywords = StringField(
        'Meta Keywords (SEO)',
        validators=[Optional(), Length(max=200)],
        render_kw={
            'placeholder': 'proteinas, ganar musculo, nutricion deportiva',
            'maxlength': '200',
            'oninput': 'updateCharCount(this, "meta-keywords-count", 200)'
        }
    )
    
    # Estado
    is_published = BooleanField(
        'Publicar',
        default=True  # Publicar por defecto
    )
