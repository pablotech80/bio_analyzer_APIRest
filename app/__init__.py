# app/__init__.py
from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Inicializar extensiones (sin app todavía)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()
csrf = CSRFProtect()
cors = CORS()


def create_app(config_name = "development"):
	"""
	Application Factory Pattern.

	Args:
			config_name: 'development', 'production', o 'testing'

	Returns:
			Flask app configurada
	"""
	app = Flask(__name__, template_folder = "templates", static_folder = "static")

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
	cors.init_app(app)

	# Configure CORS for API endpoints
	cors.init_app(
		app,
		resources = {
			r"/api/*": {
				"origins": [
					"http://localhost:3000",
					"http://localhost:5173",
					"https://*.vercel.app",
					],
				"methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
				"allow_headers": ["Content-Type", "Authorization"],
				"supports_credentials": True,
				}
			},
		)

	# Configurar Flask-Login
	login_manager.login_view = "auth.login"
	login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
	login_manager.login_message_category = "info"

	# User loader para Flask-Login
	@login_manager.user_loader
	def load_user(user_id):
		from app.models.user import User

		return User.query.get(int(user_id))

	# Registrar Blueprints
	# Auth blueprint
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

	from datetime import datetime

	app.jinja_env.globals.update(now = datetime.now)

	# Shell context para flask shell (útil para debugging)
	@app.shell_context_processor
	def make_shell_context():
		from app.models.user import Permission, Role, User

		return {"db": db, "User": User, "Role": Role, "Permission": Permission}

	@app.route('/favicon.ico')
	def favicon():
		"""Devuelve el icono del sitio."""
		return send_from_directory(
			os.path.join(app.root_path, 'static'),
			'favicon.ico',
			mimetype = 'image/vnd.microsoft.icon'
			)
	# manifiesto mcp para agent
	@app.route("/manifest", methods = ["GET"])
	def mcp_manifest():
		"""
		Devuelve la lista de herramientas disponibles para FitMaster (MCP).
		"""
		manifest = {
			"tools": [
				{
					"name": "create_analysis",
					"description": "Crea un nuevo análisis corporal con datos biométricos enviados por el usuario.",
					"server_url": "https://web-production-917c.up.railway.app",
					"path": "/api/v1/analysis",
					"method": "POST",
					"parameters": {
						"type": "object",
						"properties": {
							"weight": {"type": "number"},
							"height": {"type": "number"},
							"age": {"type": "number"},
							"gender": {"type": "string"},
							"activity_level": {"type": "string"}
							},
						"required": ["weight", "height", "age", "gender"]
						}
					},
				{
					"name": "get_history",
					"description": "Devuelve el historial completo de análisis del usuario autenticado.",
					"server_url": "https://web-production-917c.up.railway.app",
					"path": "/api/v1/history",
					"method": "GET",
					"parameters": {
						"type": "object",
						"properties": {},
						"required": []
						}
					},
				{
					"name": "get_analysis_by_id",
					"description": "Obtiene un análisis corporal específico por su ID.",
					"server_url": "https://web-production-917c.up.railway.app",
					"path": "/api/v1/analysis/{analysis_id}",
					"method": "GET",
					"parameters": {
						"type": "object",
						"properties": {
							"analysis_id": {"type": "integer"}
							},
						"required": ["analysis_id"]
						}
					}
				]
			}
		return jsonify(manifest), 200

	return app
