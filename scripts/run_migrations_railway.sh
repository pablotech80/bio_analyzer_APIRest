#!/bin/bash

# Script para ejecutar migraciones en Railway
# Uso: ./scripts/run_migrations_railway.sh

set -e  # Salir si hay error

echo "🚀 Ejecutando migraciones en Railway..."
echo ""

# Verificar si Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado"
    echo ""
    echo "Instálalo con:"
    echo "  npm i -g @railway/cli"
    echo ""
    exit 1
fi

# Verificar si está logueado
echo "📋 Verificando autenticación..."
if ! railway whoami &> /dev/null; then
    echo "❌ No estás logueado en Railway"
    echo ""
    echo "Ejecuta primero:"
    echo "  railway login"
    echo ""
    exit 1
fi

echo "✅ Autenticado correctamente"
echo ""

# Verificar estado actual
echo "📊 Estado actual de migraciones en Railway:"
railway run flask db current
echo ""

# Mostrar migraciones pendientes
echo "📋 Migraciones disponibles:"
railway run flask db heads
echo ""

# Confirmar antes de ejecutar
read -p "¿Ejecutar 'flask db upgrade' en Railway? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⚙️  Ejecutando migraciones..."
    railway run flask db upgrade
    
    echo ""
    echo "✅ Migraciones completadas"
    echo ""
    
    echo "📊 Estado final:"
    railway run flask db current
    echo ""
    
    echo "🎉 ¡Listo! Ahora puedes:"
    echo "  1. Descomentar las columnas de fotos en app/models/biometric_analysis.py"
    echo "  2. Hacer commit y push"
    echo "  3. Verificar en producción: https://app.coachbodyfit360.com"
else
    echo "❌ Operación cancelada"
    exit 0
fi
