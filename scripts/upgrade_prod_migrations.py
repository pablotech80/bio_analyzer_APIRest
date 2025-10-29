#!/usr/bin/env python3
"""
Script para ejecutar migraciones en producción (Railway PostgreSQL)
Uso: python scripts/upgrade_prod_migrations.py
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar la URL de base de datos de producción
os.environ['DATABASE_URL'] = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"
os.environ['FLASK_APP'] = 'run.py'

# Importar después de configurar las variables de entorno
from flask_migrate import upgrade
from app import create_app, db

def run_migrations():
    """Ejecutar migraciones pendientes en producción"""
    print("🚀 Ejecutando migraciones en Railway PostgreSQL...")
    print()
    
    try:
        # Crear app con configuración de producción
        app = create_app('production')
        
        with app.app_context():
            print("📊 Estado antes de migrar:")
            from flask_migrate import current
            current()
            print()
            
            # Confirmar antes de ejecutar
            response = input("¿Ejecutar 'flask db upgrade' en PRODUCCIÓN? (yes/no): ")
            
            if response.lower() != 'yes':
                print("❌ Operación cancelada")
                sys.exit(0)
            
            print("\n⚙️  Ejecutando migraciones...")
            upgrade()
            
            print("\n✅ Migraciones completadas exitosamente")
            print()
            
            print("📊 Estado después de migrar:")
            current()
            print()
            
            print("🎉 ¡Listo! Ahora puedes:")
            print("  1. Descomentar las columnas de fotos en app/models/biometric_analysis.py")
            print("  2. git add app/models/biometric_analysis.py")
            print("  3. git commit -m 'feat: Habilitar columnas de fotos después de migración'")
            print("  4. git push origin main")
            print()
            print("  Verifica en: https://app.coachbodyfit360.com")
            
    except Exception as e:
        print(f"\n❌ Error al ejecutar migraciones: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
