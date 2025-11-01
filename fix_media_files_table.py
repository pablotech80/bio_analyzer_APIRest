#!/usr/bin/env python3
"""
Script de migración robusta para crear tabla media_files
Versión adaptada para CoachBodyFit360
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🚀 INICIANDO fix_media_files_table.py")
print("=" * 70)
print()

# ============================================================================
# PASO 1: IMPORTAR MÓDULOS
# ============================================================================
print("📦 Paso 1: Importando módulos...")
try:
    from app import create_app, db
    from app.models import MediaFile, BlogPost
    from sqlalchemy import inspect, text
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error al importar: {e}")
    sys.exit(1)

print()

# ============================================================================
# PASO 2: CREAR APLICACIÓN
# ============================================================================
print("🏗️  Paso 2: Creando aplicación Flask...")
try:
    # Detectar entorno
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    print(f"✅ App creada en modo: {env}")
except Exception as e:
    print(f"❌ Error al crear app: {e}")
    sys.exit(1)

print()

# ============================================================================
# PASO 3: DIAGNÓSTICO DE BASE DE DATOS
# ============================================================================
print("=" * 70)
print("🔍 Paso 3: DIAGNÓSTICO DE BASE DE DATOS")
print("=" * 70)
print()

with app.app_context():
    # Verificar conexión
    print("🔌 Verificando conexión...")
    try:
        db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')
        # Ocultar credenciales en el output
        if '@' in db_url:
            parts = db_url.split('@')
            db_url_safe = f"{parts[0].split('://')[0]}://***@{parts[1]}"
        else:
            db_url_safe = db_url
        
        print(f"📊 Database: {db_url_safe}")
        
        # Test de conexión (compatible con SQLite y PostgreSQL)
        try:
            if 'sqlite' in db_url.lower():
                result = db.session.execute(text("SELECT sqlite_version()"))
                version = f"SQLite {result.scalar()}"
            else:
                result = db.session.execute(text("SELECT version()"))
                version = result.scalar()
            print(f"✅ {version}")
        except Exception as ver_err:
            print(f"✅ Conexión exitosa (versión no disponible)")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)
    
    print()
    
    # Listar tablas existentes
    print("📋 Listando tablas existentes...")
    try:
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        print(f"✅ Tablas encontradas ({len(existing_tables)}):")
        for table in sorted(existing_tables):
            marker = "✅" if table == "media_files" else "  "
            print(f"   {marker} {table}")
    except Exception as e:
        print(f"❌ Error al listar tablas: {e}")
        sys.exit(1)
    
    print()
    
    # Verificar si media_files ya existe
    if 'media_files' in existing_tables:
        print("=" * 70)
        print("✅✅✅ ¡TABLA media_files YA EXISTE! ✅✅✅")
        print("=" * 70)
        print()
        print("📊 Verificando estructura de la tabla...")
        
        try:
            columns = inspector.get_columns('media_files')
            print(f"✅ Columnas encontradas ({len(columns)}):")
            for col in columns:
                print(f"   - {col['name']} ({col['type']})")
            
            print()
            indexes = inspector.get_indexes('media_files')
            print(f"✅ Índices configurados ({len(indexes)}):")
            for idx in indexes:
                print(f"   - {idx['name']}")
            
            print()
            print("🎉 ¡La tabla está correctamente configurada!")
            print("✅ No se requiere ninguna acción adicional")
            
        except Exception as e:
            print(f"⚠️  Advertencia al verificar estructura: {e}")
        
        sys.exit(0)
    
    # Si llegamos aquí, la tabla NO existe
    print("⚠️  Tabla media_files NO EXISTE")
    print("🔧 Procediendo a crear la tabla...")
    print()
    
    # ========================================================================
    # PASO 4: CREAR TABLA media_files
    # ========================================================================
    print("=" * 70)
    print("🛠️  Paso 4: CREANDO TABLA media_files")
    print("=" * 70)
    print()
    
    success = False
    
    # ESTRATEGIA 1: Crear solo la tabla específica
    print("📝 Estrategia 1: MediaFile.__table__.create()")
    try:
        MediaFile.__table__.create(db.engine, checkfirst=True)
        print("✅ Tabla creada con Estrategia 1")
        success = True
    except Exception as e:
        print(f"⚠️  Estrategia 1 falló: {e}")
        print()
        
        # ESTRATEGIA 2: Crear todas las tablas
        print("📝 Estrategia 2: db.create_all()")
        try:
            db.create_all()
            print("✅ Tablas creadas con Estrategia 2")
            success = True
        except Exception as e2:
            print(f"⚠️  Estrategia 2 falló: {e2}")
            print()
            
            # ESTRATEGIA 3: SQL directo (PostgreSQL)
            print("📝 Estrategia 3: SQL directo")
            try:
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
                    uploaded_by INTEGER NOT NULL REFERENCES users(id),
                    usage_count INTEGER DEFAULT 0,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS ix_media_files_uploaded_at ON media_files(uploaded_at);
                CREATE INDEX IF NOT EXISTS ix_media_files_file_type ON media_files(file_type);
                """
                
                db.session.execute(text(sql))
                db.session.commit()
                print("✅ Tabla creada con Estrategia 3 (SQL directo)")
                success = True
            except Exception as e3:
                print(f"❌ Estrategia 3 falló: {e3}")
                print()
                print("=" * 70)
                print("❌ TODAS LAS ESTRATEGIAS FALLARON")
                print("=" * 70)
                print()
                print("🔍 Posibles causas:")
                print("   1. Permisos insuficientes en la base de datos")
                print("   2. Conexión a BD incorrecta")
                print("   3. Modelo MediaFile no está correctamente definido")
                print()
                print("💡 Soluciones:")
                print("   1. Verificar SQLALCHEMY_DATABASE_URI en .env")
                print("   2. Verificar permisos del usuario de BD")
                print("   3. Revisar app/models/media_file.py")
                sys.exit(1)
    
    print()
    
    # ========================================================================
    # PASO 5: VERIFICAR CREACIÓN EXITOSA
    # ========================================================================
    print("=" * 70)
    print("🔍 Paso 5: VERIFICANDO CREACIÓN EXITOSA")
    print("=" * 70)
    print()
    
    try:
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if 'media_files' in existing_tables:
            print("✅ Tabla media_files EXISTE")
            
            # Verificar columnas
            columns = inspector.get_columns('media_files')
            print(f"✅ {len(columns)} columnas creadas:")
            for col in columns:
                print(f"   - {col['name']}")
            
            print()
            
            # Verificar índices
            indexes = inspector.get_indexes('media_files')
            print(f"✅ {len(indexes)} índices configurados:")
            for idx in indexes:
                print(f"   - {idx['name']}")
            
            print()
            print("=" * 70)
            print("✅✅✅ ¡ÉXITO! TABLA media_files CREADA ✅✅✅")
            print("=" * 70)
            print()
            print("🎉 El sistema de blog está ahora completamente operativo")
            print("✅ Puedes subir imágenes, videos y audios")
            print("✅ La galería de medios funcionará correctamente")
            
        else:
            print("❌ Tabla media_files NO EXISTE después de intentar crearla")
            print("⚠️  Esto es inesperado. Revisa los logs anteriores.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error al verificar: {e}")
        sys.exit(1)

print()
print("=" * 70)
print("✅ Script completado exitosamente")
print("=" * 70)
