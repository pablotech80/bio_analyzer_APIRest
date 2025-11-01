#!/bin/bash
# Script de inicio para Railway
# Ejecuta init_db.py y luego inicia gunicorn

echo "=================================================="
echo "🚀 INICIANDO APLICACIÓN EN RAILWAY"
echo "=================================================="

# Forzar modo producción
export FLASK_ENV=production
echo "🔧 Ambiente: $FLASK_ENV"

# Ejecutar script para crear tablas del blog
echo ""
echo "📊 Paso 1: Creando tablas del blog..."
FLASK_ENV=production python create_blog_tables.py

# Verificar si tuvo éxito
if [ $? -eq 0 ]; then
    echo "✅ Tablas del blog creadas/verificadas correctamente"
else
    echo "⚠️  Advertencia: create_blog_tables.py falló"
fi

# Iniciar gunicorn
echo ""
echo "🌐 Paso 2: Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 run:app
