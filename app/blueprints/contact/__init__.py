# app/blueprints/contact/__init__.py
"""
Contact Blueprint
Sistema de mensajes cliente-entrenador
"""
from flask import Blueprint

from app.blueprints.contact import routes

contact_bp = Blueprint("contact", __name__, url_prefix="/contacto")
