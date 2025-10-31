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
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
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
    
    # Convertir Markdown a HTML
    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html = md.convert(content)
    
    # Sanitizar HTML (seguridad)
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
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
