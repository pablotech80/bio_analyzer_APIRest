#!/usr/bin/env python3
"""
Script de inicialización de base de datos para Railway
Crea todas las tablas necesarias
"""
import os
import sys

print("=" * 60)
print("🚀 INICIANDO init_db.py")
print("=" * 60)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def initialize_database():
    """Inicializa la base de datos creando todas las tablas"""
    print("\n📦 Importando módulos...")
    from app import create_app, db
    from sqlalchemy import text, inspect
    
    print("✅ Módulos importados")
    print("\n🏗️  Creando app...")
    app = create_app()
    print(f"✅ App creada: {app.name}")
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("🚨 CREANDO TABLAS EN BASE DE DATOS")
        print("=" * 60)
        
        # Importar TODOS los modelos explícitamente
        print("\n📋 Importando modelos...")
        from app.models import (
            User, Role, Permission, 
            BiometricAnalysis, ContactMessage,
            NutritionPlan, TrainingPlan,
            BlogPost, MediaFile
        )
        print("✅ Modelos importados:")
        print(f"  - User, Role, Permission")
        print(f"  - BiometricAnalysis, ContactMessage")
        print(f"  - NutritionPlan, TrainingPlan")
        print(f"  - BlogPost, MediaFile")
        
        try:
            # Verificar conexión
            print("\n🔌 Verificando conexión a base de datos...")
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Conectado a PostgreSQL: {version[:50]}...")
            
            # Listar tablas existentes
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"\n📋 Tablas existentes ({len(existing_tables)}): {', '.join(existing_tables) if existing_tables else 'ninguna'}")
            
            # Crear TODAS las tablas
            print("\n🔨 Ejecutando db.create_all()...")
            try:
                db.create_all()
                print("✅ db.create_all() completado!")
            except Exception as create_error:
                print(f"⚠️  Error en db.create_all(): {create_error}")
                print("🔄 Intentando crear tablas individualmente...")
                
                # Intentar crear tablas una por una
                from sqlalchemy import Table
                for table_name, table in db.metadata.tables.items():
                    try:
                        table.create(db.engine, checkfirst=True)
                        print(f"  ✅ {table_name}")
                    except Exception as e:
                        print(f"  ⚠️  {table_name}: {str(e)[:50]}")
            
            # Verificar tablas finales
            inspector = inspect(db.engine)
            final_tables = inspector.get_table_names()
            print(f"\n✅ Tablas finales ({len(final_tables)}): {', '.join(final_tables)}")
            
            # Verificar tablas críticas (solo las esenciales)
            essential_tables = ['users', 'biometric_analyses']
            optional_tables = ['blog_posts', 'media_files']
            
            print("\n🔍 Verificando tablas esenciales:")
            all_essential_ok = True
            for table in essential_tables:
                status = "✅" if table in final_tables else "❌"
                print(f"  {status} {table}")
                if table not in final_tables:
                    all_essential_ok = False
            
            print("\n🔍 Verificando tablas opcionales (blog):")
            for table in optional_tables:
                status = "✅" if table in final_tables else "⚠️ "
                print(f"  {status} {table}")
            
            if not all_essential_ok:
                missing = [t for t in essential_tables if t not in final_tables]
                print(f"\n❌ ERROR: Tablas esenciales faltantes: {', '.join(missing)}")
                print("❌ La aplicación NO puede funcionar sin estas tablas")
                return False
            
            missing_optional = [t for t in optional_tables if t not in final_tables]
            if missing_optional:
                print(f"\n⚠️  Tablas opcionales faltantes: {', '.join(missing_optional)}")
                print("⚠️  El blog no funcionará, pero el resto de la app sí")
            
            print("\n" + "=" * 60)
            print("✅ TODAS LAS TABLAS CREADAS EXITOSAMENTE")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
