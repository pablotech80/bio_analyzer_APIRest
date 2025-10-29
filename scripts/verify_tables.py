#!/usr/bin/env python3
"""
Script para verificar todas las tablas en PostgreSQL de Railway
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

# Usar red privada
DATABASE_URL = os.getenv('DATABASE_PRIVATE_URL') or os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_PRIVATE_URL o DATABASE_URL no configurada")
    print("   Ejecuta: railway run python scripts/verify_tables.py")
    sys.exit(1)

def verify_tables():
    """Verificar todas las tablas en la base de datos"""
    try:
        print("🔍 Conectando a PostgreSQL de Railway...")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("✅ Conexión exitosa\n")
            
            # Obtener todas las tablas
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Total de tablas: {len(tables)}\n")
            
            for table in sorted(tables):
                # Contar registros
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                
                # Obtener columnas
                columns = inspector.get_columns(table)
                col_count = len(columns)
                
                print(f"✅ {table}")
                print(f"   └─ {count} registros, {col_count} columnas")
                
                # Mostrar columnas importantes
                if table == 'biometric_analyses':
                    print(f"   └─ Columnas clave:")
                    for col in columns:
                        if 'photo' in col['name']:
                            print(f"      • {col['name']}: {col['type']}")
                
                print()
            
            # Verificar migración actual
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            print(f"🔖 Migración actual: {version}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_tables()
