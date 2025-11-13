#!/bin/bash
# Script rápido para conectarse a Railway PostgreSQL

echo "🔧 Conectando a Railway PostgreSQL..."
echo ""
echo "Opciones:"
echo "1. Conectar con psql (línea de comandos)"
echo "2. Ver credenciales"
echo "3. Ejecutar script Python interactivo"
echo ""
read -p "Elige una opción (1-3): " choice

case $choice in
  1)
    # Descomenta la línea DATABASE_URL en .env temporalmente
    export DATABASE_URL="postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"
    echo ""
    echo "Conectando con psql..."
    psql "$DATABASE_URL"
    ;;
  2)
    echo ""
    echo "📋 CREDENCIALES DE RAILWAY:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Host:     centerbeam.proxy.rlwy.net"
    echo "Puerto:   57147"
    echo "Database: railway"
    echo "Usuario:  postgres"
    echo "Password: engtSRttlVTDiZYzPQkRiFrnuRdgaVzg"
    echo ""
    echo "URL completa:"
    echo "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;
  3)
    export DATABASE_URL="postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"
    python connect_railway_db.py
    ;;
  *)
    echo "Opción inválida"
    ;;
esac
