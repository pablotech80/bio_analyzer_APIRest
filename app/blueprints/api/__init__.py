# app/blueprints/api/__init__.py
"""
API REST Blueprint v1
Endpoints JSON para consumo del frontend futuro
"""
from flask import Blueprint

from app.blueprints.api import routes

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
