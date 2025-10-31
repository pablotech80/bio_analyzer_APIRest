#!/usr/bin/env python3
"""
Script para ejecutar migraciones pendientes
Se ejecuta automáticamente en Railway después del deploy
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_migrations():
    """Ejecuta todas las migraciones pendientes usando Alembic"""
    from app import create_app, db
    from flask_migrate import upgrade, stamp
    from sqlalchemy import inspect
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Ejecutando migraciones de Alembic...")
        print(f"📊 Base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')[:50]}...")
        
        try:
            # Verificar si la tabla alembic_version existe
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tablas existentes: {', '.join(tables) if tables else 'ninguna'}")
            
            if 'alembic_version' not in tables:
                print("⚠️  Tabla alembic_version no existe. Inicializando...")
                # Crear todas las tablas primero
                db.create_all()
                print("✅ Tablas base creadas con db.create_all()")
                
                # Marcar como migrado a la última versión
                try:
                    stamp()
                    print("✅ Base de datos marcada con stamp()")
                except Exception as e:
                    print(f"⚠️  No se pudo hacer stamp: {e}")
            else:
                # Ejecutar migraciones normalmente
                print("🔄 Ejecutando upgrade()...")
                upgrade()
                print("✅ Migraciones de Alembic completadas!")
            
            # Verificar tablas finales
            inspector = inspect(db.engine)
            final_tables = inspector.get_table_names()
            print(f"✅ Tablas finales: {', '.join(final_tables)}")
            
            # Verificar tablas críticas
            required_tables = ['users', 'blog_posts', 'media_files']
            missing_tables = [t for t in required_tables if t not in final_tables]
            
            if missing_tables:
                print(f"⚠️  Tablas faltantes: {', '.join(missing_tables)}")
                print("🔄 Creando tablas faltantes con db.create_all()...")
                db.create_all()
                print("✅ Tablas faltantes creadas!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en migraciones: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Intentar crear tablas como fallback
            try:
                print("🔄 Fallback: Intentando crear tablas directamente...")
                db.create_all()
                print("✅ Tablas creadas con db.create_all()!")
                
                # Intentar stamp
                try:
                    stamp()
                    print("✅ Base de datos marcada con stamp()")
                except:
                    pass
                
                return True
            except Exception as e2:
                print(f"❌ Error al crear tablas: {str(e2)}")
                traceback.print_exc()
                return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)
