# app/__init__.py
"""
Factory de aplicación Flask para CoachBodyFit360
Versión mejorada con carga explícita de modelos
"""
import os
from datetime import datetime

from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

# ============================================================================
# INICIALIZACIÓN DE EXTENSIONES (sin app)
# ============================================================================
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()


# ============================================================================
# SWAGGER CONFIGURATION
# ============================================================================
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swagger = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "CoachBodyFit360 API"}
)


# ============================================================================
# APPLICATION FACTORY
# ============================================================================
def create_app(config_name=None):
    """
    Application Factory Pattern.
    Permite crear múltiples instancias de la app con diferentes configs.
    
    Args:
        config_name: Nombre de la configuración ('development', 'production', 'testing')
    
    Returns:
        Flask app configurada
    """
    app = Flask(__name__)
    
    # ========================================================================
    # 1. CARGAR CONFIGURACIÓN
    # ========================================================================
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    print(f"🔧 Configurando app en modo: {config_name}")
    
    # Mapeo de configs
    config_map = {
        "development": "app.config.DevelopmentConfig",
        "production": "app.config.ProductionConfig",
        "testing": "app.config.TestingConfig"
    }
    
    config_class = config_map.get(config_name.lower(), config_map["development"])
    app.config.from_object(config_class)
    
    # ========================================================================
    # 2. INICIALIZAR EXTENSIONES
    # ========================================================================
    print("📦 Inicializando extensiones...")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # CORS debe ir ANTES de Swagger
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    swagger.init_app(app)
    
    # ========================================================================
    # 3. IMPORTAR MODELOS EXPLÍCITAMENTE (CRÍTICO PARA db.create_all())
    # ========================================================================
    # IMPORTANTE: SQLAlchemy necesita que los modelos estén importados
    # ANTES de db.create_all() para que se registren en db.metadata
    
    with app.app_context():
        print("📋 Registrando modelos en SQLAlchemy...")
        
        # Importar TODOS los modelos para registrarlos en db.metadata
        from app.models import (
            User, Role, Permission,              # Autenticación
            BiometricAnalysis, ContactMessage,   # Core
            NutritionPlan, TrainingPlan,         # Planes
            BlogPost, MediaFile                  # Blog (CRÍTICO)
        )
        
        print("✅ Modelos registrados:")
        print("   - User, Role, Permission")
        print("   - BiometricAnalysis, ContactMessage")
        print("   - NutritionPlan, TrainingPlan")
        print("   - BlogPost, MediaFile")
        
        # Verificar que los modelos están en metadata
        table_names = [table.name for table in db.metadata.sorted_tables]
        print(f"📊 Tablas en metadata ({len(table_names)}): {', '.join(table_names)}")
    
    # ========================================================================
    # 4. CONFIGURAR FLASK-LOGIN
    # ========================================================================
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # ========================================================================
    # 5. REGISTRAR BLUEPRINTS
    # ========================================================================
    print("🔌 Registrando blueprints...")
    
    from app.blueprints.admin.routes import admin_bp
    from app.blueprints.api import api_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.bioanalyze import bioanalyze_bp
    from app.blueprints.blog import blog_bp
    from app.blueprints.contact import contact_bp
    from app.blueprints.main import main_bp
    from app.blueprints.nutrition import nutrition_bp
    from app.blueprints.training import training_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bioanalyze_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    
    print("✅ Blueprints registrados")

    # ========================================================================
    # 6. REGISTRAR ERROR HANDLERS
    # ========================================================================
    from app.middleware.error_handlers import register_error_handlers
    register_error_handlers(app)

    # ========================================================================
    # 7. JINJA GLOBALS Y FILTROS
    # ========================================================================
    app.jinja_env.globals.update(now=datetime.now)
    
    # Filtro Markdown para renderizar MD en templates
    import mistune
    from markupsafe import Markup
    
    def markdown_filter(text):
        """Convierte Markdown a HTML seguro"""
        if not text:
            return ""
        html = mistune.html(text)
        return Markup(html)
    
    app.jinja_env.filters['markdown'] = markdown_filter

    # ========================================================================
    # 8. SHELL CONTEXT
    # ========================================================================
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import Permission, Role, User
        return {"db": db, "User": User, "Role": Role, "Permission": Permission}

    # ========================================================================
    # 9. FAVICON
    # ========================================================================
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    print(f"✅ App '{app.name}' creada exitosamente")
    return app


# ============================================================================
# NOTA PARA DESARROLLADORES:
# ============================================================================
# Este archivo utiliza el patrón "Application Factory" que permite:
# 
# 1. Múltiples instancias con diferentes configuraciones
# 2. Testing más fácil (cada test puede tener su propia app)
# 3. Mejor organización del código
# 4. Evita problemas de imports circulares
#
# IMPORTANTE: Los modelos se importan dentro de app_context() para que
# SQLAlchemy los registre correctamente en db.metadata ANTES de db.create_all()
# ============================================================================
