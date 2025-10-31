from datetime import datetime

from flask import make_response, render_template

from app.utils.seo import get_landing_seo_data

from . import main_bp


@main_bp.route("/")
def landing():
    """Landing page pública con propuesta de valor"""
    seo_data = get_landing_seo_data()
    
    # Obtener últimos 3 posts del blog (con manejo de errores)
    latest_posts = []
    try:
        from app.models.blog_post import BlogPost
        latest_posts = BlogPost.query.filter_by(is_published=True)\
            .order_by(BlogPost.published_at.desc())\
            .limit(3)\
            .all()
    except Exception as e:
        # Si la tabla no existe o hay error, continuar sin posts
        print(f"Warning: No se pudieron cargar posts del blog: {e}")
    
    return render_template("main/landing.html", seo=seo_data, latest_posts=latest_posts)


@main_bp.route("/avisos-legales")
def legal_notices():
    """Avisos Legales - Información legal completa"""
    return render_template("main/legal_notices.html")


@main_bp.route("/politica-privacidad")
def privacy_policy():
    """Política de Privacidad (GDPR)"""
    return render_template("main/privacy_policy.html")


@main_bp.route("/terminos-servicio")
def terms_of_service():
    """Términos y Condiciones de Servicio"""
    return render_template("main/terms_of_service.html")


@main_bp.route("/privacidad")
def privacy():
    """Política de Privacidad (GDPR) - Ruta legacy"""
    return render_template("main/privacy.html")


@main_bp.route("/terminos")
def terms():
    """Términos y Condiciones - Ruta legacy"""
    return render_template("main/terms.html")


@main_bp.route("/sobre-nosotros")
def about():
    """Página Sobre Nosotros"""
    return render_template("main/about.html")


@main_bp.route("/sitemap.xml")
def sitemap():
    """Genera sitemap.xml dinámico para SEO."""
    sitemap_xml = render_template("sitemap.xml", now=datetime.now())
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@main_bp.route("/robots.txt")
def robots():
    """Genera robots.txt dinámico para crawlers."""
    from flask import url_for
    
    robots_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/v1/admin/
Disallow: /debug/

# Sitemap
Sitemap: {url_for('main.sitemap', _external=True)}
"""
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response
