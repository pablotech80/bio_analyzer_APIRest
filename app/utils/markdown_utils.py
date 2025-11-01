"""
Utilidades para procesar Markdown y generar contenido del blog
"""
import re
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
import bleach
from slugify import slugify


# Configuración de Markdown
MARKDOWN_EXTENSIONS = [
    'extra',  # Tablas, definiciones, etc
    'codehilite',  # Syntax highlighting
    'fenced_code',  # Bloques de código con ```
    'tables',  # Tablas
    'nl2br',  # Newline to <br>
    'sane_lists',  # Listas más inteligentes
    'md_in_html',  # Permite HTML dentro de Markdown
    TocExtension(toc_depth='2-3'),  # Tabla de contenidos
]

# Tags HTML permitidos (seguridad)
ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'strong', 'em', 'u', 'strike',
    'ul', 'ol', 'li',
    'a', 'img',
    'blockquote', 'code', 'pre',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
    'video', 'audio', 'source',  # Multimedia
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'video': ['controls', 'width', 'height', 'poster', 'preload', 'autoplay', 'loop', 'muted'],
    'audio': ['controls', 'preload', 'autoplay', 'loop', 'muted'],
    'source': ['src', 'type'],
    'code': ['class'],
    'pre': ['class'],
    'div': ['class'],
    'span': ['class'],
}


def render_markdown(content):
    """
    Convierte Markdown a HTML seguro
    
    Args:
        content (str): Contenido en Markdown
        
    Returns:
        str: HTML renderizado y sanitizado
    """
    if not content:
        return ''
    
    # Procesar videos de YouTube ANTES de markdown
    # Detectar: ![video:titulo](https://www.youtube.com/watch?v=ID) o ![video:titulo](https://youtube.com/embed/ID)
    def replace_youtube(match):
        title = match.group(1)
        url = match.group(2)
        
        # Extraer video ID
        video_id = None
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
        elif 'youtube.com/embed/' in url:
            video_id = url.split('embed/')[1].split('?')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        
        if video_id:
            return f'<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 2rem 0;"><iframe src="https://www.youtube.com/embed/{video_id}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
        return match.group(0)
    
    content = re.sub(r'!\[video:([^\]]+)\]\(([^)]+youtube[^)]+)\)', replace_youtube, content)
    
    # Convertir Markdown a HTML
    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html = md.convert(content)
    
    # Sanitizar HTML (seguridad) - Agregar iframe a tags permitidos
    allowed_tags = ALLOWED_TAGS + ['iframe']
    allowed_attrs = ALLOWED_ATTRIBUTES.copy()
    allowed_attrs['iframe'] = ['src', 'frameborder', 'allow', 'allowfullscreen', 'style']
    allowed_attrs['div'] = ['class', 'style']
    
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    return clean_html


def calculate_reading_time(content):
    """
    Calcula el tiempo estimado de lectura
    
    Args:
        content (str): Contenido en Markdown
        
    Returns:
        int: Minutos estimados de lectura
    """
    if not content:
        return 0
    
    # Remover Markdown syntax para contar palabras reales
    text = re.sub(r'[#*`\[\]()]', '', content)
    words = len(text.split())
    
    # Promedio: 200 palabras por minuto
    minutes = max(1, round(words / 200))
    
    return minutes


def generate_slug(title):
    """
    Genera un slug URL-friendly desde el título
    
    Args:
        title (str): Título del post
        
    Returns:
        str: Slug generado
    """
    if not title:
        return ''
    
    # Usar slugify para generar slug limpio
    slug = slugify(title, max_length=100)
    
    return slug


def extract_first_image(content):
    """
    Extrae la primera imagen del contenido Markdown
    
    Args:
        content (str): Contenido en Markdown
        
    Returns:
        str|None: URL de la primera imagen o None
    """
    if not content:
        return None
    
    # Buscar patrón ![alt](url)
    match = re.search(r'!\[.*?\]\((.*?)\)', content)
    
    if match:
        return match.group(1)
    
    return None


def generate_excerpt(content, max_length=200):
    """
    Genera un excerpt (resumen) desde el contenido
    
    Args:
        content (str): Contenido en Markdown
        max_length (int): Longitud máxima del excerpt
        
    Returns:
        str: Excerpt generado
    """
    if not content:
        return ''
    
    # Remover Markdown syntax
    text = re.sub(r'[#*`\[\]()!]', '', content)
    
    # Remover líneas vacías múltiples
    text = re.sub(r'\n+', ' ', text)
    
    # Truncar a max_length
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text.strip()


def extract_headings(content):
    """
    Extrae todos los headings (H2, H3) para generar tabla de contenidos
    
    Args:
        content (str): Contenido en Markdown
        
    Returns:
        list: Lista de diccionarios con {level, text, id}
    """
    if not content:
        return []
    
    headings = []
    
    # Buscar headings ## y ###
    for match in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2).strip()
        heading_id = slugify(text)
        
        headings.append({
            'level': level,
            'text': text,
            'id': heading_id
        })
    
    return headings
