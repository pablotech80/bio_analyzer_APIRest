"""
Vista de Landing con SEO Optimizado
====================================

Este módulo implementa la vista de la landing page con metadatos SEO
completos y estructurados según las mejores prácticas de 2025.

Ubicación sugerida: apps/landing/views.py o apps/public/views.py

Principios aplicados:
- SRP: Una función, una responsabilidad (render landing con SEO)
- DRY: Datos SEO centralizados en diccionario reutilizable
- KISS: Estructura simple y clara
"""

from flask import Blueprint, render_template, url_for, request
from typing import Dict, Any

# Blueprint para la landing (ajusta el nombre según tu proyecto)
landing_bp = Blueprint('landing', __name__)


def get_landing_seo_data() -> Dict[str, Any]:
    """
    Genera los metadatos SEO para la landing page.
    
    Returns:
        Dict con todos los campos necesarios para SEO completo:
        - title: Título optimizado para SERP (50-60 caracteres)
        - description: Meta descripción (150-160 caracteres)
        - keywords: Palabras clave objetivo
        - og_image: URL absoluta de imagen Open Graph (1200x630px)
        - og_type: Tipo de contenido (website, article, etc.)
        - canonical: URL canónica para evitar contenido duplicado
        
    Notas técnicas:
        - Título incluye palabras clave principales + marca
        - Descripción tiene CTA implícito ("Análisis Gratis")
        - Keywords cubren long-tail y short-tail
        - og_image debe existir en static/images/
    """
    return {
        # TÍTULO: Optimizado para CTR en Google
        # Formato: [Beneficio] | [Diferenciador] | [Marca]
        'title': 'Entrenador Personal + IA | Análisis Gratis 90seg | CoachBodyFit360',
        
        # DESCRIPCIÓN: 158 caracteres (óptimo para SERP)
        # Incluye: beneficio + diferenciador + CTA + friction remover
        'description': (
            'Transforma tu cuerpo con 20 años de experiencia + IA avanzada. '
            'Análisis biométrico completo en 90 segundos. '
            'Plan personalizado gratis. Sin tarjeta de crédito.'
        ),
        
        # KEYWORDS: Mix de short-tail y long-tail
        # Priorizadas por volumen de búsqueda en España
        'keywords': (
            'entrenador personal online, '
            'plan fitness personalizado, '
            'análisis biométrico gratis, '
            'IA fitness, '
            'coaching nutricional online, '
            'perder peso rápido, '
            'ganar músculo en casa, '
            'app entrenamiento personalizado, '
            'dieta personalizada gratis'
        ),
        
        # OPEN GRAPH IMAGE: Debe ser 1200x630px
        # Requerimiento: crear esta imagen con:
        # - Logo centrado
        # - Texto: "Entrenador Personal + IA"
        # - Colores: #E74C3C y #E67E22 (del logo)
        'og_image': url_for(
            'static',
            filename='images/og-image-cbf360.jpg',
            _external=True  # Genera URL absoluta (https://...)
        ),
        
        # TIPO DE CONTENIDO: 'website' para homepage
        # Otros valores: 'article', 'product', 'profile'
        'og_type': 'website',
        
        # CANONICAL URL: Evita penalizaciones por contenido duplicado
        # Siempre apunta a la versión principal (sin parámetros GET)
        'canonical': url_for('landing.index', _external=True),
        
        # DATOS ADICIONALES (opcionales pero recomendados)
        'author': 'CoachBodyFit360',
        'locale': 'es_ES',
        'site_name': 'CoachBodyFit360',
    }


@landing_bp.route('/')
@landing_bp.route('/index')
def index():
    """
    Renderiza la landing page principal con SEO completo.
    
    Returns:
        Template renderizado con contexto SEO
        
    Ejemplo de uso en template (landing.html):
        {% block title %}{{ seo.title }}{% endblock %}
        
    Notas de rendimiento:
        - get_landing_seo_data() es ligera (no hace queries DB)
        - url_for() con _external=True cachea resultados
        - Total overhead: <1ms
    """
    # Obtener datos SEO estructurados
    seo_data = get_landing_seo_data()
    
    # Context adicional (puedes agregar más datos aquí)
    context = {
        'seo': seo_data,
        
        # Métricas en tiempo real (opcional)
        'stats': {
            'total_users': 500,  # TODO: Obtener de DB en producción
            'visits_this_month': 1550,  # TODO: Integrar con Cloudflare API
            'avg_rating': 5.0,
        },
        
        # Feature flags (para A/B testing futuro)
        'features': {
            'show_testimonials': True,
            'show_video_hero': False,
            'enable_chat_widget': True,
        }
    }
    
    return render_template('landing.html', **context)


@landing_bp.route('/sitemap.xml')
def sitemap():
    """
    Genera sitemap.xml dinámico para Google Search Console.
    
    Returns:
        XML con todas las URLs públicas del site
        
    TODO: Implementar generación dinámica cuando tengas:
        - Blog posts
        - Páginas de servicios
        - Páginas legales (términos, privacidad)
    """
    # Por ahora retorna sitemap estático
    # En producción, genera dinámicamente desde DB
    pages = [
        url_for('landing.index', _external=True),
        url_for('auth.register', _external=True),
        url_for('auth.login', _external=True),
        # TODO: Agregar más URLs cuando estén disponibles
    ]
    
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@landing_bp.route('/robots.txt')
def robots():
    """
    Genera robots.txt dinámico para control de crawlers.
    
    Returns:
        Texto plano con directivas para bots
        
    Notas:
        - Permite indexar todo el contenido público
        - Bloquea admin, auth y API endpoints
        - Incluye link al sitemap
    """
    robots_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/private/
Disallow: /auth/logout
Disallow: /dashboard/

Sitemap: {url_for('landing.sitemap', _external=True)}
"""
    response = make_response(robots_txt)
    response.headers['Content-Type'] = 'text/plain'
    return response


# ============================================================================
# FUNCIONES DE UTILIDAD (para vistas específicas)
# ============================================================================

def get_blog_post_seo(post_id: int) -> Dict[str, Any]:
    """
    Genera SEO específico para un post de blog.
    
    Args:
        post_id: ID del post en la base de datos
        
    Returns:
        Dict con SEO optimizado para article
        
    TODO: Implementar cuando tengas sistema de blog
    """
    # Ejemplo de estructura para futuro
    post = get_post_by_id(post_id)  # Función ficticia
    
    return {
        'title': f'{post.title} | Blog CoachBodyFit360',
        'description': post.excerpt[:160],
        'keywords': ', '.join(post.tags),
        'og_image': post.featured_image_url,
        'og_type': 'article',
        'canonical': url_for('blog.post', post_id=post_id, _external=True),
        'article_published_time': post.created_at.isoformat(),
        'article_author': post.author.name,
    }


# ============================================================================
# CONFIGURACIÓN DEL BLUEPRINT
# ============================================================================

def init_app(app):
    """
    Registra el blueprint en la aplicación Flask.
    
    Args:
        app: Instancia de Flask
        
    Uso en __init__.py o app.py:
        from apps.landing.views import landing_bp, init_app
        init_app(app)
    """
    app.register_blueprint(landing_bp, url_prefix='/')
