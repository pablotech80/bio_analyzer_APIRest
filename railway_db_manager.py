#!/usr/bin/env python3
"""
Script para gestionar la base de datos de Railway PostgreSQL
Uso: python railway_db_manager.py
"""
import os
from sqlalchemy import create_engine, text, inspect

# URL de Railway (desde tu .env comentado)
RAILWAY_DB_URL = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"

def connect():
    """Conecta a la base de datos"""
    try:
        engine = create_engine(RAILWAY_DB_URL, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Conectado a Railway PostgreSQL")
            print(f"📌 {version.split(',')[0]}\n")
        return engine
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None

def show_tables(engine):
    """Muestra todas las tablas"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📋 Tablas ({len(tables)}):")
    for table in sorted(tables):
        print(f"   • {table}")
    return tables

def show_users(engine):
    """Muestra usuarios"""
    print("\n" + "="*70)
    print("👥 USUARIOS")
    print("="*70)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, email, first_name, last_name, is_admin, created_at 
            FROM users 
            ORDER BY id
        """))
        
        for row in result:
            admin = "👑 ADMIN" if row[4] else "👤 Usuario"
            print(f"\n[{row[0]}] {row[1]}")
            print(f"    Nombre: {row[2]} {row[3]}")
            print(f"    Rol: {admin}")
            print(f"    Creado: {row[5]}")

def show_analyses(engine):
    """Muestra análisis biométricos"""
    print("\n" + "="*70)
    print("📈 ANÁLISIS BIOMÉTRICOS (últimos 10)")
    print("="*70)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT ba.id, ba.user_id, u.email, ba.weight, ba.height, 
                   ba.has_fitmaster_data, ba.created_at
            FROM biometric_analysis ba
            JOIN users u ON ba.user_id = u.id
            ORDER BY ba.created_at DESC
            LIMIT 10
        """))
        
        for row in result:
            fitmaster = "🤖 FitMaster" if row[5] else "📊 Básico"
            print(f"\n[{row[0]}] Usuario: {row[2]} (ID: {row[1]})")
            print(f"    Peso: {row[3]} kg | Altura: {row[4]} cm")
            print(f"    Tipo: {fitmaster}")
            print(f"    Fecha: {row[6]}")

def show_messages(engine):
    """Muestra mensajes de contacto"""
    print("\n" + "="*70)
    print("💬 MENSAJES DE CONTACTO (últimos 10)")
    print("="*70)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT cm.id, u.email, cm.subject, cm.is_read, cm.created_at
            FROM contact_messages cm
            JOIN users u ON cm.user_id = u.id
            ORDER BY cm.created_at DESC
            LIMIT 10
        """))
        
        for row in result:
            status = "✅ Leído" if row[3] else "🔔 Nuevo"
            print(f"\n[{row[0]}] De: {row[1]}")
            print(f"    Asunto: {row[2]}")
            print(f"    Estado: {status}")
            print(f"    Fecha: {row[4]}")

def execute_query(engine):
    """Ejecuta consultas SQL personalizadas"""
    print("\n" + "="*70)
    print("🔧 CONSOLA SQL INTERACTIVA")
    print("="*70)
    print("Escribe tu consulta SQL (o 'exit' para salir)")
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
                
                if query.strip().upper().startswith('SELECT'):
                    rows = result.fetchall()
                    if rows:
                        print(f"\n✅ {len(rows)} resultados:")
                        for row in rows:
                            print(f"   {row}")
                    else:
                        print("\n✅ Sin resultados.")
                else:
                    conn.commit()
                    print(f"\n✅ Consulta ejecutada.")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    print("="*70)
    print("🚀 RAILWAY DATABASE MANAGER")
    print("="*70)
    print()
    
    engine = connect()
    if not engine:
        return
    
    tables = show_tables(engine)
    
    if 'users' in tables:
        show_users(engine)
    
    if 'biometric_analysis' in tables:
        show_analyses(engine)
    
    if 'contact_messages' in tables:
        show_messages(engine)
    
    print("\n" + "="*70)
    print("MENÚ")
    print("="*70)
    print("1. Ejecutar consulta SQL")
    print("2. Salir")
    
    choice = input("\nOpción: ").strip()
    
    if choice == '1':
        execute_query(engine)
    
    print("\n✅ Desconectado.")

if __name__ == "__main__":
    main()
