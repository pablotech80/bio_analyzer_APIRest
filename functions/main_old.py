import sys
from pathlib import Path

from flask import redirect, url_for

# Esto asume que la carpeta 'src' está DENTRO de la carpeta 'functions'
sys.path.append(str(Path(__file__).resolve().parent))

from flask import Flask
from src.body_analyzer.routes import all_blueprints

# Configuración de Flask como constante
FLASK_CONFIG = {
    "DEBUG": False, # Es buena práctica ponerlo en False para producción
    "JSON_SORT_KEYS": False,
}

def register_blueprints(app):
    """Registra todos los blueprints en la aplicación Flask."""
    for bp in all_blueprints:
        app.register_blueprint(bp)

def create_app():
    app = Flask(
        __name__,
        # Las plantillas y archivos estáticos se sirven desde la carpeta 'public' de Firebase
        # por lo que estas líneas ya no son necesarias en el entorno de la nube.
        # template_folder='templates',
        # static_folder='static'
        )
    app.secret_key = 'bioanalyze_super_secret_key'
    app.config.update(FLASK_CONFIG)
    register_blueprints(app)

    @app.route("/")
    def index():
        return redirect(url_for("informe_web.informe_web"))

    return app

app = create_app()

# --- CÓDIGO AÑADIDO PARA FIREBASE ---
# Este es el "envoltorio" que convierte tu app de Flask en una Cloud Function
# llamada "api", que es el nombre que pusimos en firebase.json.

from firebase_functions import https_fn

@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
  return app(req.environ, req.start_response)