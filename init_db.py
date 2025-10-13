# init_db.py
from app import create_app, db


def initialize_database():
    """Inicializa la base de datos si no existe."""
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print(
                "✅ Base de datos inicializada correctamente (solo tablas faltantes)."
            )
        except Exception as e:
            print("⚠️ Error al inicializar la base de datos:", e)


if __name__ == "__main__":
    initialize_database()
