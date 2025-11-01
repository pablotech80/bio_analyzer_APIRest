#!/usr/bin/env python3
"""
Script de Verificación del Blog - verify_blog_system.py
Diagnóstico completo del sistema de blog y media files

Este script verifica:
1. Conexión a la base de datos
2. Existencia de tablas del blog
3. Estructura de la tabla media_files
4. Modelos correctamente importados
5. Blueprints registrados
6. Configuración de almacenamiento
"""
import os
import sys

print("=" * 70)
print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE BLOG")
print("=" * 70)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def verify_blog_system():
    """Verifica el estado completo del sistema de blog"""
    
    issues = []
    warnings = []
    success_count = 0
    
    # ========================================================================
    # 1. IMPORTAR Y CREAR APP
    # ========================================================================
    print("\n📦 1. IMPORTANDO MÓDULOS...")
    try:
        from app import create_app, db
        from sqlalchemy import text, inspect
        print("✅ Módulos importados correctamente")
        success_count += 1
    except Exception as e:
        print(f"❌ Error al importar: {str(e)}")
        issues.append(f"Import error: {str(e)}")
        return issues, warnings
    
    print("\n🏗️  2. CREANDO APLICACIÓN...")
    try:
        env = os.environ.get("FLASK_ENV", "development")
        if os.environ.get("RAILWAY_ENVIRONMENT"):
            env = "production"
        
        app = create_app(env)
        print(f"✅ App creada en modo: {env}")
        success_count += 1
    except Exception as e:
        print(f"❌ Error al crear app: {str(e)}")
        issues.append(f"App creation error: {str(e)}")
        return issues, warnings
    
    with app.app_context():
        # ====================================================================
        # 2. VERIFICAR CONEXIÓN A BD
        # ====================================================================
        print("\n🔌 3. VERIFICANDO CONEXIÓN A BASE DE DATOS...")
        try:
            db_url = str(db.engine.url)
            
            # Ocultar password
            if "@" in db_url:
                parts = db_url.split("@")
                db_url_safe = parts[0].split("://")[0] + "://***@" + parts[1]
            else:
                db_url_safe = db_url
            
            print(f"   📊 Database: {db_url_safe}")
            
            is_postgres = 'postgresql' in db_url
            is_sqlite = 'sqlite' in db_url
            
            with db.engine.connect() as conn:
                if is_postgres:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"   ✅ PostgreSQL: {version[:50]}...")
                elif is_sqlite:
                    result = conn.execute(text("SELECT sqlite_version()"))
                    version = result.fetchone()[0]
                    print(f"   ✅ SQLite: v{version}")
                else:
                    print(f"   ✅ Base de datos: {db.engine.dialect.name}")
            
            success_count += 1
        
        except Exception as e:
            print(f"   ❌ Error de conexión: {str(e)}")
            issues.append(f"Database connection error: {str(e)}")
            return issues, warnings
        
        # ====================================================================
        # 3. VERIFICAR TABLAS
        # ====================================================================
        print("\n📋 4. VERIFICANDO TABLAS DEL BLOG...")
        try:
            inspector = inspect(db.engine)
            all_tables = inspector.get_table_names()
            
            blog_tables = {
                'blog_posts': False,
                'media_files': False
            }
            
            for table in blog_tables.keys():
                if table in all_tables:
                    blog_tables[table] = True
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table} - NO EXISTE")
                    issues.append(f"Tabla '{table}' no existe")
            
            if all(blog_tables.values()):
                print("   ✅ Todas las tablas del blog existen")
                success_count += 1
            else:
                missing = [t for t, exists in blog_tables.items() if not exists]
                warnings.append(f"Tablas faltantes: {', '.join(missing)}")
        
        except Exception as e:
            print(f"   ❌ Error al verificar tablas: {str(e)}")
            issues.append(f"Table verification error: {str(e)}")
        
        # ====================================================================
        # 4. VERIFICAR ESTRUCTURA DE media_files
        # ====================================================================
        if 'media_files' in all_tables:
            print("\n📊 5. VERIFICANDO ESTRUCTURA DE media_files...")
            try:
                columns = inspector.get_columns('media_files')
                
                required_columns = [
                    'id', 'filename', 'file_path', 'file_url',
                    'file_type', 'mime_type', 'file_size',
                    'title', 'alt_text', 'caption',
                    'width', 'height', 'duration',
                    'uploaded_by', 'usage_count', 'uploaded_at'
                ]
                
                column_names = [col['name'] for col in columns]
                
                print(f"   📋 Columnas encontradas ({len(column_names)}):")
                for col in columns:
                    nullable = "NULL" if col.get('nullable', True) else "NOT NULL"
                    pk = " (PK)" if col.get('primary_key') else ""
                    print(f"      - {col['name']:<20} {str(col['type']):<20} {nullable}{pk}")
                
                missing_cols = set(required_columns) - set(column_names)
                if missing_cols:
                    print(f"   ⚠️  Columnas faltantes: {', '.join(missing_cols)}")
                    warnings.append(f"Columnas faltantes en media_files: {', '.join(missing_cols)}")
                else:
                    print("   ✅ Todas las columnas requeridas existen")
                    success_count += 1
                
                # Verificar índices
                indexes = inspector.get_indexes('media_files')
                print(f"\n   🎯 Índices ({len(indexes)}):")
                for idx in indexes:
                    print(f"      - {idx['name']}: {idx['column_names']}")
                
                if len(indexes) >= 2:
                    print("   ✅ Índices configurados correctamente")
                    success_count += 1
                else:
                    warnings.append("Faltan índices en media_files")
            
            except Exception as e:
                print(f"   ❌ Error al verificar estructura: {str(e)}")
                issues.append(f"Structure verification error: {str(e)}")
        else:
            print("\n⚠️  5. TABLA media_files NO EXISTE - Saltando verificación de estructura")
        
        # ====================================================================
        # 5. VERIFICAR MODELOS
        # ====================================================================
        print("\n📋 6. VERIFICANDO MODELOS...")
        try:
            from app.models import (
                User, Role, Permission,
                BiometricAnalysis, ContactMessage,
                NutritionPlan, TrainingPlan,
                BlogPost, MediaFile
            )
            
            print("   ✅ User, Role, Permission")
            print("   ✅ BiometricAnalysis, ContactMessage")
            print("   ✅ NutritionPlan, TrainingPlan")
            print("   ✅ BlogPost, MediaFile")
            
            # Verificar que están en metadata
            table_names_metadata = [table.name for table in db.metadata.sorted_tables]
            
            if 'blog_posts' in table_names_metadata:
                print("   ✅ BlogPost registrado en metadata")
            else:
                warnings.append("BlogPost no está en db.metadata")
            
            if 'media_files' in table_names_metadata:
                print("   ✅ MediaFile registrado en metadata")
            else:
                warnings.append("MediaFile no está en db.metadata")
            
            success_count += 1
        
        except ImportError as e:
            print(f"   ❌ Error al importar modelos: {str(e)}")
            issues.append(f"Model import error: {str(e)}")
        
        # ====================================================================
        # 6. VERIFICAR BLUEPRINTS
        # ====================================================================
        print("\n🔌 7. VERIFICANDO BLUEPRINTS...")
        try:
            blueprints = list(app.blueprints.keys())
            print(f"   📋 Blueprints registrados ({len(blueprints)}):")
            for bp in blueprints:
                print(f"      - {bp}")
            
            if 'blog' in blueprints:
                print("   ✅ Blueprint 'blog' registrado")
                success_count += 1
            else:
                print("   ❌ Blueprint 'blog' NO registrado")
                issues.append("Blueprint 'blog' no está registrado")
        
        except Exception as e:
            print(f"   ❌ Error al verificar blueprints: {str(e)}")
            issues.append(f"Blueprint verification error: {str(e)}")
        
        # ====================================================================
        # 7. VERIFICAR CONFIGURACIÓN DE ALMACENAMIENTO
        # ====================================================================
        print("\n💾 8. VERIFICANDO CONFIGURACIÓN DE ALMACENAMIENTO...")
        try:
            upload_folder = app.config.get('UPLOAD_FOLDER')
            max_content_length = app.config.get('MAX_CONTENT_LENGTH')
            allowed_extensions = app.config.get('ALLOWED_EXTENSIONS', set())
            
            print(f"   📁 UPLOAD_FOLDER: {upload_folder}")
            print(f"   📏 MAX_CONTENT_LENGTH: {max_content_length / (1024*1024):.0f} MB" if max_content_length else "   ⚠️  MAX_CONTENT_LENGTH: No configurado")
            print(f"   📄 Extensiones permitidas: {', '.join(allowed_extensions) if allowed_extensions else 'No configurado'}")
            
            if upload_folder and os.path.exists(upload_folder):
                print(f"   ✅ Carpeta de uploads existe: {upload_folder}")
                success_count += 1
            elif upload_folder:
                print(f"   ⚠️  Carpeta de uploads NO existe: {upload_folder}")
                warnings.append(f"Carpeta {upload_folder} no existe")
            else:
                print("   ⚠️  UPLOAD_FOLDER no configurado")
                warnings.append("UPLOAD_FOLDER no configurado")
            
            # Verificar variables de S3 (si están configuradas)
            s3_bucket = os.environ.get('AWS_BUCKET_NAME')
            if s3_bucket:
                print(f"\n   ☁️  Configuración S3 detectada:")
                print(f"      - Bucket: {s3_bucket}")
                print(f"      - Region: {os.environ.get('AWS_REGION', 'No configurado')}")
                print(f"      - Access Key: {'Configurado' if os.environ.get('AWS_ACCESS_KEY_ID') else 'No configurado'}")
            else:
                print("\n   📁 Almacenamiento local (sin S3)")
        
        except Exception as e:
            print(f"   ❌ Error al verificar configuración: {str(e)}")
            warnings.append(f"Storage config error: {str(e)}")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    
    print(f"\n✅ Verificaciones exitosas: {success_count}/8")
    
    if issues:
        print(f"\n❌ PROBLEMAS CRÍTICOS ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    if warnings:
        print(f"\n⚠️  ADVERTENCIAS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    if not issues and not warnings:
        print("\n🎉 ¡TODO ESTÁ PERFECTO!")
        print("✅ El blog está 100% operativo")
    elif issues:
        print("\n⚠️  SE REQUIERE ACCIÓN INMEDIATA")
        print("❌ El blog NO funcionará correctamente")
    else:
        print("\n✅ El blog debería funcionar")
        print("⚠️  Hay algunos detalles menores a revisar")
    
    return issues, warnings


if __name__ == "__main__":
    try:
        issues, warnings = verify_blog_system()
        
        print("\n" + "=" * 70)
        if not issues:
            print("✅ VERIFICACIÓN COMPLETADA")
            print("=" * 70)
            if warnings:
                print("\n📝 Hay algunas advertencias, pero el sistema debería funcionar")
            sys.exit(0)
        else:
            print("❌ VERIFICACIÓN FALLÓ")
            print("=" * 70)
            print("\n📝 Se encontraron problemas críticos que deben resolverse")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
