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
from flask_migrate import upgrade

def run_migrations():
    """Ejecuta todas las migraciones pendientes usando Alembic"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Ejecutando migraciones de Alembic...")
        
        try:
            # Ejecutar migraciones de Alembic
            upgrade()
            print("✅ Migraciones de Alembic completadas exitosamente!")
            
            # Crear cualquier tabla que falte (fallback)
            db.create_all()
            print("✅ Verificación de tablas completada!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en migraciones: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Intentar crear tablas como fallback
            try:
                print("🔄 Intentando crear tablas directamente...")
                db.create_all()
                print("✅ Tablas creadas exitosamente!")
                return True
            except Exception as e2:
                print(f"❌ Error al crear tablas: {str(e2)}")
                return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)
