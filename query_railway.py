#!/usr/bin/env python3
"""
Script simple para consultar Railway PostgreSQL
Uso: python query_railway.py "SELECT * FROM users"
"""
import sys
from sqlalchemy import create_engine, text

RAILWAY_DB_URL = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"

def execute_query(query):
    """Ejecuta una consulta SQL"""
    try:
        engine = create_engine(RAILWAY_DB_URL, echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            
            if query.strip().upper().startswith('SELECT'):
                rows = result.fetchall()
                if rows:
                    print(f"\n✅ {len(rows)} resultados:\n")
                    for row in rows:
                        print(row)
                else:
                    print("\n✅ Sin resultados.")
            else:
                conn.commit()
                print(f"\n✅ Consulta ejecutada exitosamente.")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python query_railway.py \"SELECT * FROM users\"")
        print("\nEjemplos:")
        print('  python query_railway.py "SELECT * FROM users LIMIT 5"')
        print('  python query_railway.py "SELECT COUNT(*) FROM biometric_analyses"')
        print('  python query_railway.py "SELECT * FROM contact_messages WHERE is_read = false"')
    else:
        query = " ".join(sys.argv[1:])
        execute_query(query)
