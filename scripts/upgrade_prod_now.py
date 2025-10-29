#!/usr/bin/env python3
"""
Script para ejecutar migraciones en producción SIN confirmación
USAR CON PRECAUCIÓN - Ejecuta migraciones directamente
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar la URL de base de datos de producción
os.environ['DATABASE_URL'] = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"
os.environ['FLASK_APP'] = 'run.py'

# Importar después de configurar las variables de entorno
from flask_migrate import upgrade, current as show_current
from app import create_app

def run_migrations():
    """Ejecutar migraciones pendientes en producción"""
    print("🚀 Ejecutando migraciones en Railway PostgreSQL...")
    print()
    
    try:
        # Crear app con configuración de producción
        app = create_app('production')
        
        with app.app_context():
            print("📊 Estado ANTES de migrar:")
            show_current()
            print()
            
            print("⚙️  Ejecutando 'flask db upgrade'...")
            upgrade()
            
            print("\n✅ Migraciones completadas exitosamente")
            print()
            
            print("📊 Estado DESPUÉS de migrar:")
            show_current()
            print()
            
            # Verificar que las columnas existen
            from sqlalchemy import text
            from app import db
            
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'biometric_analyses' 
                AND column_name IN ('front_photo_url', 'back_photo_url', 'side_photo_url')
                ORDER BY column_name;
            """))
            
            photo_columns = [row[0] for row in result]
            
            print("📸 Verificación de columnas de fotos:")
            for col in ['front_photo_url', 'back_photo_url', 'side_photo_url']:
                status = "✅" if col in photo_columns else "❌"
                print(f"   {status} {col}")
            
            print()
            
            if len(photo_columns) == 3:
                print("🎉 ¡ÉXITO! Todas las columnas de fotos fueron creadas")
                print()
                print("📝 PRÓXIMOS PASOS:")
                print("  1. Descomentar las columnas en app/models/biometric_analysis.py (líneas 219-235)")
                print("  2. git add app/models/biometric_analysis.py")
                print("  3. git commit -m 'feat: Habilitar columnas de fotos después de migración'")
                print("  4. git push origin main")
                print()
                print("  ✅ Verifica en: https://app.coachbodyfit360.com")
            else:
                print("⚠️  Algunas columnas no se crearon correctamente")
                
    except Exception as e:
        print(f"\n❌ Error al ejecutar migraciones: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("⚠️  ADVERTENCIA: Este script ejecutará migraciones en PRODUCCIÓN")
    print("   Base de datos: Railway PostgreSQL")
    print("   Migraciones a aplicar: 8d34854ebd24 → c18eb18a660c → 581cd9ed2c74")
    print()
    run_migrations()
