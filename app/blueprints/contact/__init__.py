# app/blueprints/contact/__init__.py
"""
Contact Blueprint
Sistema de mensajes cliente-entrenador
"""
from flask import Blueprint

contact_bp = Blueprint('contact', __name__, url_prefix='/contacto')

from app.blueprints.contact import routes
