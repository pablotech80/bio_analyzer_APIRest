#!/usr/bin/env python3
"""
Script para obtener y mostrar las credenciales de Railway
"""
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def parse_database_url(url):
    """Parsea la URL de la base de datos y muestra las credenciales"""
    if not url:
        return None
    
    try:
        parsed = urlparse(url)
        
        # Validar que sea una URL real de PostgreSQL
        if not parsed.hostname or parsed.hostname == 'host':
            return None
        
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/'),
            'username': parsed.username,
            'password': parsed.password,
            'full_url': url
        }
    except Exception as e:
        print(f"⚠️  Error al parsear URL: {e}")
        return None

def main():
    print("="*70)
    print("🔑 CREDENCIALES DE RAILWAY POSTGRESQL")
    print("="*70)
    
    # Intentar obtener DATABASE_PRIVATE_URL (recomendado)
    private_url = os.environ.get('DATABASE_PRIVATE_URL')
    public_url = os.environ.get('DATABASE_URL')
    
    if private_url:
        print("\n✅ DATABASE_PRIVATE_URL encontrada (Red privada - SIN cargos de egress)")
        print("-"*70)
        creds = parse_database_url(private_url)
        if creds:
            print(f"Host:     {creds['host']}")
            print(f"Puerto:   {creds['port']}")
            print(f"Database: {creds['database']}")
            print(f"Usuario:  {creds['username']}")
            print(f"Password: {creds['password']}")
            print(f"\nURL completa:\n{creds['full_url']}")
    
    if public_url:
        print("\n⚠️  DATABASE_URL encontrada (Red pública - Genera cargos de egress)")
        print("-"*70)
        creds = parse_database_url(public_url)
        if creds:
            print(f"Host:     {creds['host']}")
            print(f"Puerto:   {creds['port']}")
            print(f"Database: {creds['database']}")
            print(f"Usuario:  {creds['username']}")
            print(f"Password: {creds['password']}")
            print(f"\nURL completa:\n{creds['full_url']}")
    
    if not private_url and not public_url:
        print("\n❌ No se encontraron credenciales de Railway en .env")
        print("\n📝 Para obtenerlas:")
        print("1. Ve a https://railway.app")
        print("2. Selecciona tu proyecto 'CoachBodyFit360'")
        print("3. Haz clic en el servicio 'PostgreSQL'")
        print("4. Ve a la pestaña 'Variables'")
        print("5. Busca 'DATABASE_PRIVATE_URL' (recomendado) o 'DATABASE_URL'")
        print("6. Copia el valor y agrégalo a tu archivo .env:")
        print("\n   DATABASE_PRIVATE_URL=postgresql://usuario:password@host:puerto/database")
        return
    
    # Comando para conectar con psql
    print("\n" + "="*70)
    print("🔧 COMANDOS PARA CONECTAR")
    print("="*70)
    
    if private_url:
        print("\n1️⃣  Conectar con psql (línea de comandos):")
        print(f'   psql "{private_url}"')
        
        print("\n2️⃣  Conectar con Python (SQLAlchemy):")
        print(f'   from sqlalchemy import create_engine')
        print(f'   engine = create_engine("{private_url}")')
        
        print("\n3️⃣  Usar el script connect_railway_db.py:")
        print(f'   python connect_railway_db.py')
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
