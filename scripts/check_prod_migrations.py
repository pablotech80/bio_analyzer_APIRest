#!/usr/bin/env python3
"""
Script para verificar el estado de migraciones en producción
Uso: python scripts/check_prod_migrations.py
"""

import os
import sys
from sqlalchemy import create_engine, text

# URL de producción (Railway PostgreSQL)
# Usar DATABASE_PRIVATE_URL para evitar cargos de egress
DATABASE_URL = os.getenv('DATABASE_PRIVATE_URL') or os.getenv('DATABASE_URL')

if not DATABASE_URL or DATABASE_URL == 'None':
    print("❌ ERROR: DATABASE_PRIVATE_URL o DATABASE_URL no está configurada")
    print("   Ejecuta: railway run python scripts/check_prod_migrations.py")
    sys.exit(1)

def check_migrations():
    """Verificar estado de migraciones en producción"""
    try:
        print("🔍 Conectando a PostgreSQL de Railway...")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("✅ Conexión exitosa\n")
            
            # Verificar si existe la tabla alembic_version
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            
            if not result.scalar():
                print("❌ Tabla alembic_version no existe")
                print("   La base de datos no tiene migraciones inicializadas")
                return
            
            # Obtener versión actual
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            current_version = result.scalar()
            
            print(f"📊 Migración actual en producción: {current_version}")
            print()
            
            # Verificar si existen las columnas de fotos
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'biometric_analyses' 
                AND column_name IN ('front_photo_url', 'back_photo_url', 'side_photo_url')
                ORDER BY column_name;
            """))
            
            photo_columns = [row[0] for row in result]
            
            print("📸 Estado de columnas de fotos:")
            for col in ['front_photo_url', 'back_photo_url', 'side_photo_url']:
                status = "✅ Existe" if col in photo_columns else "❌ Falta"
                print(f"   {col}: {status}")
            
            print()
            
            if len(photo_columns) == 3:
                print("🎉 ¡Todas las columnas de fotos existen!")
                print("   Puedes descomentar las columnas en el modelo")
            else:
                print("⚠️  Faltan columnas de fotos")
                print("   Necesitas ejecutar: flask db upgrade")
            
            # Verificar todas las columnas de biometric_analyses
            print("\n📋 Todas las columnas de biometric_analyses:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'biometric_analyses'
                ORDER BY ordinal_position;
            """))
            
            for row in result:
                nullable = "NULL" if row[2] == 'YES' else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} ({nullable})")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_migrations()
