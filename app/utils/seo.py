"""
Utilidades SEO para CoachBodyFit360
Genera metadatos optimizados para motores de búsqueda y redes sociales.
"""

from flask import url_for
from typing import Dict, Any


def get_landing_seo_data() -> Dict[str, Any]:
    """
    Genera metadatos SEO optimizados para la landing page.
    
    Incluye:
    - Meta tags básicos (title, description, keywords)
    - Open Graph tags (Facebook, LinkedIn)
    - Twitter Cards
    - Canonical URL
    
    Returns:
        Dict con todos los campos SEO necesarios
    """
    # Generar URL de imagen y forzar HTTPS
    og_image_url = url_for(
        'static',
        filename='images/og-image-cbf360.jpg',
        _external=True
    ).replace('http://', 'https://')
    
    canonical_url = url_for('main.landing', _external=True).replace('http://', 'https://')
    
    return {
        'title': 'Entrenador Personal + IA | Análisis Gratis 90seg | CoachBodyFit360',
        'description': (
            'Transforma tu cuerpo con 20 años de experiencia + IA avanzada. '
            'Análisis biométrico completo en 90 segundos. '
            'Plan personalizado gratis. Sin tarjeta de crédito.'
        ),
        'keywords': (
            'entrenador personal online, plan fitness personalizado, '
            'análisis biométrico gratis, IA fitness, coaching nutricional, '
            'plan entrenamiento personalizado, nutrición deportiva, '
            'transformación corporal, entrenador personal España'
        ),
        'og_image': og_image_url,
        'og_image_alt': 'CoachBodyFit360 - Entrenador Personal con IA - Análisis Biométrico Gratis',
        'og_type': 'website',
        'canonical': canonical_url,
    }


def get_page_seo_data(
    title: str,
    description: str,
    keywords: str = None,
    og_type: str = 'website'
) -> Dict[str, Any]:
    """
    Genera metadatos SEO para páginas específicas.
    
    Args:
        title: Título de la página
        description: Descripción meta
        keywords: Keywords separadas por comas (opcional)
        og_type: Tipo de Open Graph (default: 'website')
    
    Returns:
        Dict con campos SEO
    """
    return {
        'title': f'{title} | CoachBodyFit360',
        'description': description,
        'keywords': keywords or 'CoachBodyFit360, fitness, entrenamiento',
        'og_image': url_for(
            'static',
            filename='images/og-image-cbf360.jpg',
            _external=True
        ),
        'og_type': og_type,
        'canonical': url_for('main.landing', _external=True),
    }
