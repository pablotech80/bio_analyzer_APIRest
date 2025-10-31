#!/usr/bin/env python3
"""
Script para ejecutar migraciones pendientes
Se ejecuta automáticamente en Railway después del deploy
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import BlogPost, MediaFile

def run_migrations():
    """Ejecuta todas las migraciones pendientes"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Ejecutando migraciones...")
        
        try:
            # Crear todas las tablas
            db.create_all()
            print("✅ Migraciones completadas exitosamente!")
            print("\n📊 Tablas creadas/verificadas:")
            print("  - blog_posts")
            print("  - media_files")
            print("  - (y todas las demás tablas existentes)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en migraciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)
