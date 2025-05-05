from flask import Flask, redirect, url_for
from src.body_analyzer.routes import all_blueprints

FLASK_CONFIG = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False,
}

def register_blueprints(app):
    for bp in all_blueprints:
        app.register_blueprint(bp)

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.secret_key = 'bioanalyze_super_secret_key'
    app.config.update(FLASK_CONFIG)

    register_blueprints(app)

    @app.route("/")
    def index():
        return redirect(url_for("informe_web.informe_web"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
