"""
Blueprint para gestión de planes de entrenamiento personalizados.
"""
from flask import Blueprint

training_bp = Blueprint('training', __name__, url_prefix='/entrenamiento')

from . import routes
