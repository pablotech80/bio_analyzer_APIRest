#!/bin/bash
# Script de inicio para Railway
# Ejecuta init_db.py y luego inicia gunicorn

echo "=================================================="
echo "🚀 INICIANDO APLICACIÓN EN RAILWAY"
echo "=================================================="

# Forzar modo producción
export DJANGO_SETTINGS_MODULE=config.settings.production
echo "🔧 DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Ejecutar migraciones de base de datos
echo ""
echo "📊 Paso 1: Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

# Verificar si tuvo éxito
if [ $? -eq 0 ]; then
    echo "✅ Migraciones aplicadas correctamente"
else
    echo "⚠️  Advertencia: python manage.py migrate falló"
fi

# Iniciar gunicorn
echo ""
echo "🌐 Paso 3: Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 300 config.wsgi:application
