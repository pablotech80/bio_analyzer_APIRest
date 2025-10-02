from pathlib import Path

from flask import Flask, redirect, url_for

from src.body_analyzer.routes import all_blueprints

FLASK_CONFIG = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False,
}


def register_blueprints(app: Flask) -> None:
    """Registrar todos los blueprints disponibles en la aplicación."""
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parents[2] / "templates"),
        static_folder=str(Path(__file__).resolve().parents[2] / "static"),
    )
    app.secret_key = "bioanalyze_super_secret_key"
    app.config.update(FLASK_CONFIG)
    register_blueprints(app)

    @app.route("/")
    def index():
        return redirect(url_for("informe_web.informe_web"))

    return app


def _create_default_app() -> Flask:
    """Separa la creación del objeto app para reutilizarla en los tests."""
    return create_app()


app = _create_default_app()

__all__ = ["app", "create_app"]
