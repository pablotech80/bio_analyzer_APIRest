from flask import Blueprint
from app import csrf

telegram_bp = Blueprint("telegram", __name__)
csrf.exempt(telegram_bp)

from . import routes
