#!/usr/bin/env python3
"""
Script para conectarse a la base de datos de Railway (PostgreSQL)
Uso: python connect_railway_db.py
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Cargar variables de entorno
load_dotenv()

def get_database_url():
    """Obtiene la URL de la base de datos de Railway"""
    # Railway provee DATABASE_PRIVATE_URL (recomendado) o DATABASE_URL
    db_url = os.environ.get('DATABASE_PRIVATE_URL') or os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ ERROR: No se encontró DATABASE_PRIVATE_URL ni DATABASE_URL en .env")
        print("\nPara obtener las credenciales:")
        print("1. Ve a https://railway.app")
        print("2. Selecciona tu proyecto")
        print("3. Selecciona el servicio PostgreSQL")
        print("4. Ve a la pestaña 'Variables'")
        print("5. Copia DATABASE_PRIVATE_URL y agrégala a tu archivo .env")
        return None
    
    # Corregir formato si es necesario (postgres:// -> postgresql://)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    return db_url

def show_database_info(engine):
    """Muestra información de la base de datos"""
    print("\n" + "="*60)
    print("📊 INFORMACIÓN DE LA BASE DE DATOS")
    print("="*60)
    
    inspector = inspect(engine)
    
    # Listar todas las tablas
    tables = inspector.get_table_names()
    print(f"\n📋 Tablas encontradas ({len(tables)}):")
    for table in sorted(tables):
        print(f"   • {table}")
    
    return tables

def show_users(engine):
    """Muestra todos los usuarios"""
    print("\n" + "="*60)
    print("👥 USUARIOS")
    print("="*60)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, email, first_name, last_name, is_admin, created_at 
            FROM users 
            ORDER BY id
        """))
        
        users = result.fetchall()
        if not users:
            print("No hay usuarios en la base de datos")
            return
        
        for user in users:
            admin_badge = "👑 ADMIN" if user[4] else "👤 Usuario"
            print(f"\nID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Nombre: {user[2]} {user[3]}")
            print(f"   Rol: {admin_badge}")
            print(f"   Creado: {user[5]}")

def show_analyses(engine):
    """Muestra los análisis biométricos"""
    print("\n" + "="*60)
    print("📈 ANÁLISIS BIOMÉTRICOS")
    print("="*60)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT ba.id, ba.user_id, u.email, ba.weight, ba.height, 
                   ba.has_fitmaster_data, ba.created_at
            FROM biometric_analysis ba
            JOIN users u ON ba.user_id = u.id
            ORDER BY ba.created_at DESC
            LIMIT 10
        """))
        
        analyses = result.fetchall()
        if not analyses:
            print("No hay análisis en la base de datos")
            return
        
        print(f"\nÚltimos {len(analyses)} análisis:")
        for analysis in analyses:
            fitmaster = "🤖 FitMaster" if analysis[5] else "📊 Básico"
            print(f"\nID: {analysis[0]}")
            print(f"   Usuario: {analysis[2]} (ID: {analysis[1]})")
            print(f"   Peso: {analysis[3]} kg | Altura: {analysis[4]} cm")
            print(f"   Tipo: {fitmaster}")
            print(f"   Fecha: {analysis[6]}")

def show_messages(engine):
    """Muestra los mensajes de contacto"""
    print("\n" + "="*60)
    print("💬 MENSAJES DE CONTACTO")
    print("="*60)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT cm.id, u.email, cm.subject, cm.is_read, cm.created_at
            FROM contact_messages cm
            JOIN users u ON cm.user_id = u.id
            ORDER BY cm.created_at DESC
            LIMIT 10
        """))
        
        messages = result.fetchall()
        if not messages:
            print("No hay mensajes en la base de datos")
            return
        
        print(f"\nÚltimos {len(messages)} mensajes:")
        for msg in messages:
            status = "✅ Leído" if msg[3] else "🔔 Nuevo"
            print(f"\nID: {msg[0]}")
            print(f"   De: {msg[1]}")
            print(f"   Asunto: {msg[2]}")
            print(f"   Estado: {status}")
            print(f"   Fecha: {msg[4]}")

def execute_custom_query(engine):
    """Permite ejecutar consultas SQL personalizadas"""
    print("\n" + "="*60)
    print("🔧 EJECUTAR CONSULTA SQL PERSONALIZADA")
    print("="*60)
    print("\nEscribe tu consulta SQL (o 'exit' para salir):")
    print("Ejemplo: SELECT * FROM users LIMIT 5;\n")
    
    while True:
        query = input("SQL> ").strip()
        
        if query.lower() in ['exit', 'quit', 'salir']:
            break
        
        if not query:
            continue
        
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query))
                
                # Si es un SELECT, mostrar resultados
                if query.strip().upper().startswith('SELECT'):
                    rows = result.fetchall()
                    if rows:
                        print(f"\n✅ {len(rows)} resultados:")
                        for row in rows:
                            print(f"   {row}")
                    else:
                        print("\n✅ Consulta ejecutada. Sin resultados.")
                else:
                    # Para INSERT, UPDATE, DELETE
                    conn.commit()
                    print(f"\n✅ Consulta ejecutada exitosamente.")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    print("🚀 Conectando a Railway PostgreSQL...")
    
    # Obtener URL de la base de datos
    db_url = get_database_url()
    if not db_url:
        return
    
    try:
        # Crear engine de SQLAlchemy
        engine = create_engine(db_url, echo=False)
        
        # Probar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Conectado exitosamente!")
            print(f"📌 PostgreSQL: {version.split(',')[0]}")
        
        # Mostrar información
        tables = show_database_info(engine)
        
        # Mostrar datos si existen las tablas
        if 'users' in tables:
            show_users(engine)
        
        if 'biometric_analysis' in tables:
            show_analyses(engine)
        
        if 'contact_messages' in tables:
            show_messages(engine)
        
        # Menú interactivo
        print("\n" + "="*60)
        print("🔧 OPCIONES")
        print("="*60)
        print("1. Ejecutar consulta SQL personalizada")
        print("2. Salir")
        
        choice = input("\nElige una opción (1-2): ").strip()
        
        if choice == '1':
            execute_custom_query(engine)
        
        print("\n✅ Desconectado de la base de datos.")
        
    except Exception as e:
        print(f"\n❌ Error al conectar: {e}")
        print("\nVerifica que:")
        print("1. DATABASE_PRIVATE_URL esté correctamente configurada en .env")
        print("2. Tu IP esté permitida en Railway (si aplica)")
        print("3. Las credenciales sean correctas")

if __name__ == "__main__":
    main()
