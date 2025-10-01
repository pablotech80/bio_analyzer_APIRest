# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

# Inicializar extensiones (sin app todavía)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()
csrf = CSRFProtect()


def create_app(config_name = 'development'):
	"""
	Application Factory Pattern.

	Args:
		config_name: 'development', 'production', o 'testing'

	Returns:
		Flask app configurada
	"""
	app = Flask(
		__name__,
		template_folder = 'templates',
		static_folder = 'static'
		)

	# Cargar configuración
	from app.config import config_by_name
	app.config.from_object(config_by_name[config_name])

	# Inicializar extensiones con la app
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)
	csrf.init_app(app)

	# Configurar Flask-Login
	login_manager.login_view = 'auth.login'
	login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
	login_manager.login_message_category = 'info'

	# User loader para Flask-Login
	@login_manager.user_loader
	def load_user(user_id):
		from app.models.user import User
		return User.query.get(int(user_id))

	# Registrar Blueprints
	with app.app_context():
		# Auth blueprint
		from app.blueprints.auth import auth_bp
		app.register_blueprint(auth_bp, url_prefix = '/auth')

		# BioAnalyze blueprint (migrar el existente después)
		# from app.blueprints.bioanalyze import bioanalyze_bp
		# app.register_blueprint(bioanalyze_bp, url_prefix='/bioanalyze')

		# API blueprint
		# from app.blueprints.api import api_bp
		# app.register_blueprint(api_bp, url_prefix='/api/v1')

		# Ruta principal temporal
		@app.route('/')
		def index():
			from flask import render_template
			return render_template('index.html')

	# Registrar error handlers
	from app.middleware.error_handlers import register_error_handlers
	register_error_handlers(app)

	from datetime import datetime
	app.jinja_env.globals.update(now = datetime.now)

	# Shell context para flask shell (útil para debugging)
	@app.shell_context_processor
	def make_shell_context():
		from app.models.user import User, Role, Permission
		return {
			'db': db,
			'User': User,
			'Role': Role,
			'Permission': Permission
			}

	return app