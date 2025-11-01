#!/usr/bin/env python3
"""
Script de Migración Robusta - fix_media_files_table.py
Versión mejorada que GARANTIZA la creación de la tabla media_files

Este script:
1. Verifica la conexión a la base de datos
2. Lista tablas existentes
3. Importa explícitamente el modelo MediaFile
4. Crea la tabla si no existe
5. Verifica que la creación fue exitosa
"""
import os
import sys

print("=" * 70)
print("🔧 SCRIPT DE MIGRACIÓN: fix_media_files_table.py")
print("=" * 70)

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def fix_media_files_table():
    """Migración robusta para tabla media_files"""
    
    print("\n📦 Paso 1: Importando módulos...")
    from app import create_app, db
    from sqlalchemy import text, inspect
    
    print("✅ Módulos importados correctamente")
    
    print("\n🏗️  Paso 2: Creando aplicación Flask...")
    # Forzar modo production si estamos en Railway
    env = os.environ.get("FLASK_ENV", "development")
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        env = "production"
    
    app = create_app(env)
    print(f"✅ App creada en modo: {env}")
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("🔍 Paso 3: DIAGNÓSTICO DE BASE DE DATOS")
        print("=" * 70)
        
        # ====================================================================
        # VERIFICAR CONEXIÓN
        # ====================================================================
        try:
            print("\n🔌 Verificando conexión...")
            db_url = str(db.engine.url)
            
            # Ocultar password de la URL
            if "@" in db_url:
                parts = db_url.split("@")
                db_url_safe = parts[0].split("://")[0] + "://***:***@" + parts[1]
            else:
                db_url_safe = db_url
            
            print(f"📊 Database: {db_url_safe}")
            
            # Detectar tipo de BD
            is_postgres = 'postgresql' in db_url
            is_sqlite = 'sqlite' in db_url
            
            with db.engine.connect() as conn:
                if is_postgres:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"✅ PostgreSQL: {version[:60]}...")
                elif is_sqlite:
                    result = conn.execute(text("SELECT sqlite_version()"))
                    version = result.fetchone()[0]
                    print(f"✅ SQLite: v{version}")
                else:
                    print(f"✅ Base de datos: {db.engine.dialect.name}")
        
        except Exception as e:
            print(f"❌ ERROR de conexión: {str(e)}")
            return False
        
        # ====================================================================
        # LISTAR TABLAS EXISTENTES
        # ====================================================================
        try:
            print("\n📋 Listando tablas existentes...")
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"✅ Tablas encontradas ({len(existing_tables)}):")
            for table in existing_tables:
                print(f"   - {table}")
            
            # Verificar si media_files ya existe
            if 'media_files' in existing_tables:
                print("\n✅ ¡Tabla 'media_files' YA EXISTE!")
                print("ℹ️  No se requiere migración. El blog debería funcionar correctamente.")
                
                # Mostrar estructura de la tabla
                print("\n📊 Estructura de la tabla 'media_files':")
                columns = inspector.get_columns('media_files')
                for col in columns:
                    print(f"   - {col['name']}: {col['type']} {'(PK)' if col.get('primary_key') else ''}")
                
                return True
            else:
                print("\n⚠️  Tabla 'media_files' NO EXISTE. Procediendo con la migración...")
        
        except Exception as e:
            print(f"❌ ERROR al listar tablas: {str(e)}")
            return False
        
        # ====================================================================
        # IMPORTAR MODELOS EXPLÍCITAMENTE
        # ====================================================================
        print("\n" + "=" * 70)
        print("📋 Paso 4: IMPORTANDO MODELOS")
        print("=" * 70)
        
        try:
            # Importar TODOS los modelos para registrarlos
            from app.models import (
                User, Role, Permission,
                BiometricAnalysis, ContactMessage,
                NutritionPlan, TrainingPlan,
                BlogPost, MediaFile  # <-- CRÍTICO
            )
            
            print("✅ Modelos importados:")
            print("   - User, Role, Permission")
            print("   - BiometricAnalysis, ContactMessage")
            print("   - NutritionPlan, TrainingPlan")
            print("   - BlogPost, MediaFile")
            
            # Verificar que MediaFile está en metadata
            table_names = [table.name for table in db.metadata.sorted_tables]
            print(f"\n📊 Tablas en db.metadata ({len(table_names)}):")
            for table in table_names:
                marker = "✅" if table in existing_tables else "⚠️ "
                print(f"   {marker} {table}")
            
            if 'media_files' not in table_names:
                print("\n❌ ERROR: MediaFile no está registrado en db.metadata")
                print("⚠️  Esto indica un problema de importación del modelo")
                return False
        
        except Exception as e:
            print(f"❌ ERROR al importar modelos: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        # ====================================================================
        # CREAR TABLA media_files
        # ====================================================================
        print("\n" + "=" * 70)
        print("🔨 Paso 5: CREANDO TABLA media_files")
        print("=" * 70)
        
        try:
            # Opción 1: Crear solo la tabla media_files
            print("\n🔧 Ejecutando MediaFile.__table__.create()...")
            MediaFile.__table__.create(db.engine, checkfirst=True)
            print("✅ Comando ejecutado")
            
            # Verificar que se creó
            inspector = inspect(db.engine)
            final_tables = inspector.get_table_names()
            
            if 'media_files' in final_tables:
                print("\n" + "=" * 70)
                print("✅✅✅ ¡ÉXITO! TABLA media_files CREADA ✅✅✅")
                print("=" * 70)
                
                # Mostrar estructura
                print("\n📊 Estructura de la tabla creada:")
                columns = inspector.get_columns('media_files')
                for col in columns:
                    nullable = "NOT NULL" if not col.get('nullable', True) else "NULL"
                    pk = "(PK)" if col.get('primary_key') else ""
                    print(f"   - {col['name']:<20} {str(col['type']):<20} {nullable:<10} {pk}")
                
                print("\n🎯 Índices creados:")
                indexes = inspector.get_indexes('media_files')
                for idx in indexes:
                    print(f"   - {idx['name']}: {idx['column_names']}")
                
                print("\n✅ El blog ya puede usar la tabla media_files")
                print("✅ Puedes subir imágenes, videos y audios")
                
                return True
            else:
                print("\n❌ ERROR: La tabla NO se creó")
                print("⚠️  Intentando método alternativo...")
                
                # Opción 2: Usar db.create_all()
                print("\n🔧 Ejecutando db.create_all()...")
                db.create_all()
                
                # Verificar de nuevo
                inspector = inspect(db.engine)
                final_tables = inspector.get_table_names()
                
                if 'media_files' in final_tables:
                    print("✅ Tabla creada con db.create_all()")
                    return True
                else:
                    print("❌ Tabla aún no existe después de db.create_all()")
                    
                    # Opción 3: SQL directo (último recurso)
                    if is_postgres:
                        print("\n🔧 Último intento: Ejecutando SQL directo...")
                        
                        sql = """
                        CREATE TABLE IF NOT EXISTS media_files (
                            id SERIAL PRIMARY KEY,
                            filename VARCHAR(255) NOT NULL,
                            file_path VARCHAR(500) NOT NULL UNIQUE,
                            file_url VARCHAR(500) NOT NULL,
                            file_type VARCHAR(50) NOT NULL,
                            mime_type VARCHAR(100),
                            file_size INTEGER,
                            title VARCHAR(200),
                            alt_text VARCHAR(200),
                            caption VARCHAR(500),
                            width INTEGER,
                            height INTEGER,
                            duration INTEGER,
                            uploaded_by INTEGER NOT NULL,
                            usage_count INTEGER DEFAULT 0,
                            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (uploaded_by) REFERENCES users(id)
                        );
                        
                        CREATE INDEX IF NOT EXISTS ix_media_files_file_path 
                            ON media_files(file_path);
                        CREATE INDEX IF NOT EXISTS ix_media_files_uploaded_at 
                            ON media_files(uploaded_at);
                        """
                        
                        with db.engine.connect() as conn:
                            conn.execute(text(sql))
                            conn.commit()
                        
                        print("✅ SQL directo ejecutado")
                        
                        # Verificar una última vez
                        inspector = inspect(db.engine)
                        final_tables = inspector.get_table_names()
                        
                        if 'media_files' in final_tables:
                            print("✅ Tabla creada con SQL directo")
                            return True
                    
                    return False
        
        except Exception as e:
            print(f"\n❌ ERROR al crear tabla: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 INICIANDO MIGRACIÓN")
    print("=" * 70)
    
    success = fix_media_files_table()
    
    print("\n" + "=" * 70)
    if success:
        print("✅✅✅ MIGRACIÓN COMPLETADA CON ÉXITO ✅✅✅")
        print("=" * 70)
        print("\n📝 Próximos pasos:")
        print("   1. Reinicia la aplicación")
        print("   2. Accede a /blog/admin")
        print("   3. Intenta subir una imagen")
        print("   4. Verifica que se guarda en la tabla media_files")
        sys.exit(0)
    else:
        print("❌❌❌ MIGRACIÓN FALLÓ ❌❌❌")
        print("=" * 70)
        print("\n📝 Qué hacer:")
        print("   1. Revisa los errores arriba")
        print("   2. Verifica la conexión a la base de datos")
        print("   3. Asegúrate de que el modelo MediaFile existe")
        print("   4. Contacta al equipo de desarrollo")
        sys.exit(1)
