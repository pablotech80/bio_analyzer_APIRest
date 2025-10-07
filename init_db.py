# init_db.py
"""Script para inicializar la base de datos en Railway"""
import os

os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from flask_migrate import upgrade

app = create_app('production')

with app.app_context():
	print("🔄 Ejecutando migraciones...")
	upgrade()
	print("✅ Migraciones completadas")

	print("🔄 Creando tablas si no existen...")
	db.create_all()
	print("✅ Base de datos lista")