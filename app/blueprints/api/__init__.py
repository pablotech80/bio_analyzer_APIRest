# app/blueprints/api/__init__.py
"""
API REST Blueprint v1
Endpoints JSON para consumo del frontend futuro
"""
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

from app.blueprints.api import routes
