# app/__init__.py
import os # Importa os si no lo tienes
from flask import Flask, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS # Importa CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flasgger import Swagger

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()
csrf = CSRFProtect()
cors = CORS() # <--- 2. INICIALIZA CORS
swagger = Swagger() # <--- 3. INICIALIZA Swagger

def create_app(config_name="development"):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones CON LA APP
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)
    # NO llames a cors.init_app(app) sin 'resources' aquí

    # ---> 4. CONFIGURA CORS ANTES de Flasgger <---
    cors.init_app(
        app,
        resources={
            # Permite a OpenAI leer el esquema OpenAPI generado por Flasgger
            r"/apidocs/*": { # Flasgger sirve en /apidocs/ y /apidocs/openapi.json
                "origins": ["https://chat.openai.com"], # Permite SOLO a OpenAI
                "methods": ["GET"],
                "allow_headers": ["Content-Type"],
            },
            # Mantiene tu configuración API existente (puedes añadir OpenAI si es necesario)
            r"/api/*": {
                "origins": [
                    "http://localhost:3000", # Tus frontends
                    "http://localhost:5173",
                    "https://*.vercel.app",
                    "https://chat.openai.com" # Si el agente llama directamente a tu API
                ],
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            },
            # Opcional: Permitir acceso a archivos estáticos si fuera necesario
            # r"/static/*": {
            #     "origins": "*" # O orígenes específicos
            # }
        },
        supports_credentials=True # Habilita credenciales globalmente
    )

    # ---> 5. INICIALIZA Swagger DESPUÉS de CORS <---
    swagger.init_app(app)

    # Configurar Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
       from app.models.user import User
       return User.query.get(int(user_id))

    # Registrar Blueprints
    from app.blueprints.admin.routes import admin_bp
    from app.blueprints.api import api_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.bioanalyze import bioanalyze_bp
    from app.blueprints.contact import contact_bp
    from app.blueprints.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(bioanalyze_bp)
    app.register_blueprint(api_bp, url_prefix = "/api/v1")
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    # Registrar error handlers
    from app.middleware.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Jinja globals
    from datetime import datetime
    app.jinja_env.globals.update(now = datetime.now)

    @app.shell_context_processor
    def make_shell_context():
       from app.models.user import Permission, Role, User
       return {"db": db, "User": User, "Role": Role, "Permission": Permission}

    @app.route('/favicon.ico')
    def favicon():
       return send_from_directory(
          os.path.join(app.root_path, 'static'),
          'favicon.ico',
          mimetype = 'image/vnd.microsoft.icon'
          )

    return app