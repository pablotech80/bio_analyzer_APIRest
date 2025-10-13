# app/blueprints/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="../../templates/auth")

from app.blueprints.auth import routes  # noqa: E402, F401
