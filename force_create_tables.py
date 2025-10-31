#!/usr/bin/env python3
"""
Script de emergencia para crear tablas faltantes
Ejecutar manualmente si run_migrations.py falla
"""
import os
import sys

print("=" * 60)
print("🚀 INICIANDO force_create_tables.py")
print("=" * 60)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def force_create_tables():
    """Fuerza la creación de todas las tablas"""
    print("\n📦 Importando módulos...")
    from app import create_app, db
    from sqlalchemy import text
    
    print("✅ Módulos importados")
    print("\n🏗️  Creando app...")
    app = create_app()
    print(f"✅ App creada: {app.name}")
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("🚨 FORZANDO CREACIÓN DE TABLAS")
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
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Conectado a PostgreSQL: {version[:50]}...")
            
            # Listar tablas existentes
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"\n📋 Tablas existentes ({len(existing_tables)}): {', '.join(existing_tables)}")
            
            # Crear TODAS las tablas definidas en los modelos
            print("\n🔨 Creando todas las tablas con db.create_all()...")
            db.create_all()
            print("✅ db.create_all() ejecutado!")
            
            # Verificar tablas después
            inspector = inspect(db.engine)
            final_tables = inspector.get_table_names()
            print(f"\n✅ Tablas finales ({len(final_tables)}): {', '.join(final_tables)}")
            
            # Verificar tablas críticas
            critical_tables = ['users', 'blog_posts', 'media_files', 'biometric_analyses']
            print("\n🔍 Verificando tablas críticas:")
            for table in critical_tables:
                status = "✅" if table in final_tables else "❌"
                print(f"  {status} {table}")
            
            missing = [t for t in critical_tables if t not in final_tables]
            if missing:
                print(f"\n⚠️  ADVERTENCIA: Tablas faltantes: {', '.join(missing)}")
                return False
            
            print("\n" + "=" * 60)
            print("✅ TODAS LAS TABLAS CREADAS EXITOSAMENTE")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = force_create_tables()
    sys.exit(0 if success else 1)
