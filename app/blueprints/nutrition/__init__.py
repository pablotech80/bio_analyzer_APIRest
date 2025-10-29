"""
Blueprint para gestión de planes nutricionales personalizados.
"""
from flask import Blueprint

nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/nutricion')

from . import routes
