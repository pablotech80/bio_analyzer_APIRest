#!/bin/bash
# Script de inicio para Railway
# Ejecuta init_db.py y luego inicia gunicorn

echo "=================================================="
echo "🚀 INICIANDO APLICACIÓN EN RAILWAY"
echo "=================================================="

# Forzar modo producción
export FLASK_ENV=production
echo "🔧 Ambiente: $FLASK_ENV"

# Ejecutar init_db.py para crear tablas
echo ""
echo "📊 Paso 1: Inicializando base de datos..."
FLASK_ENV=production python init_db.py

# Verificar y crear tabla media_files si no existe
echo ""
echo "🔧 Paso 1.5: Verificando tabla media_files..."
FLASK_ENV=production python -c "
from app import create_app, db
from sqlalchemy import text, inspect

app = create_app('production')
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'media_files' not in tables:
        print('⚠️  Tabla media_files no existe. Creando...')
        with open('create_media_files_table.sql', 'r') as f:
            sql = f.read()
            db.session.execute(text(sql))
            db.session.commit()
        print('✅ Tabla media_files creada')
    else:
        print('✅ Tabla media_files ya existe')
"

# Verificar si init_db.py tuvo éxito
if [ $? -eq 0 ]; then
    echo "✅ Base de datos inicializada correctamente"
else
    echo "⚠️  Advertencia: init_db.py falló, pero continuando..."
fi

# Iniciar gunicorn
echo ""
echo "🌐 Paso 2: Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 run:app
