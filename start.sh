#!/bin/bash
# Script de inicio para Railway
# Ejecuta init_db.py y luego inicia gunicorn

echo "=================================================="
echo "🚀 INICIANDO APLICACIÓN EN RAILWAY"
echo "=================================================="

# Forzar modo producción
export FLASK_ENV=production
echo "🔧 Ambiente: $FLASK_ENV"

# Ejecutar migraciones de Flask
echo ""
echo "📊 Paso 1: Ejecutando migraciones de base de datos..."
FLASK_ENV=production flask db upgrade

# Verificar si las migraciones tuvieron éxito
if [ $? -eq 0 ]; then
    echo "✅ Migraciones ejecutadas correctamente"
else
    echo "⚠️  Advertencia: Migraciones fallaron, intentando init_db.py..."
    FLASK_ENV=production python init_db.py
fi

# Iniciar gunicorn
echo ""
echo "🌐 Paso 2: Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 run:app
