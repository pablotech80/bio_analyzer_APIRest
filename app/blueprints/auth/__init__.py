# app/blueprints/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

# Importar rutas después de crear el blueprint para evitar import circular
from app.blueprints.auth import routes