from flask import Blueprint

bioanalyze_bp = Blueprint(
    "bioanalyze",
    __name__,
    template_folder="templates",
)

from . import routes  # noqa: E402,F401
