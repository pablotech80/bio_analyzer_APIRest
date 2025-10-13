from flask import render_template

from . import main_bp


@main_bp.route("/")
def landing():
    """Landing page pública con propuesta de valor"""
    return render_template("main/landing.html")


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
