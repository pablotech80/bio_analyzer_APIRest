import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask
from body_analyzer.routes import all_blueprints  # Correcto desde dentro de src

# Configuración de Flask como constante
FLASK_CONFIG = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False,
}

def register_blueprints(app):
    """Registra todos los blueprints en la aplicación Flask."""
    for bp in all_blueprints:
        app.register_blueprint(bp)

def create_app():
    app = Flask(__name__)
    app.config.update(FLASK_CONFIG)
    register_blueprints(app)

    @app.route("/")
    def welcome_message():
        return "Bienvenido a la API Bio Analyzer"

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
