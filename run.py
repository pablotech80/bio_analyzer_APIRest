# run.py
"""
Entry point de la aplicación CoachBodyFit360.
"""
import os

from app import create_app, db

# Determinar el entorno (por defecto development)
config_name = os.environ.get("FLASK_ENV", "development")

# Crear la aplicación
app = create_app(config_name)




@app.cli.command()
def init_db():
	"""Inicializar la base de datos (crear tablas)."""
	db.create_all()



@app.cli.command()
def seed_db():
	"""Poblar la base de datos con datos de prueba."""
	from scripts.init_roles import init_roles_and_permissions

	with app.app_context():
		# Inicializar roles
		init_roles_and_permissions()

		# Crear un usuario admin de prueba
		from app.blueprints.auth.services import AuthService

		try:
			admin = AuthService.register_user(
				username = "admin",
				email = "admin@coachbodyfit360.com",
				password = "Admin123!",
				first_name = "Administrador",
				last_name = "Sistema",
				)

			# Asignar rol admin
			from app.models.user import Role

			admin_role = Role.query.filter_by(name = "admin").first()
			admin.role = admin_role
			db.session.commit()


		except ValueError as e:

			print(f"ℹ️  Usuario admin ya existe: {e}")


if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0", port = 5000)
