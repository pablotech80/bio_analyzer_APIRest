"""
Blueprint del Blog
"""
from flask import Blueprint

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

# Importar rutas después de crear el blueprint para evitar imports circulares
from app.blueprints.blog import routes, admin_routes
