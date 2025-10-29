#!/usr/bin/env python3
"""
Script para verificar planes nutricionales en producción
"""

import os
import sys
from sqlalchemy import create_engine, text

# URL de producción
DATABASE_URL = os.getenv('DATABASE_URL') or "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"

def check_nutrition_plans():
    """Verificar planes nutricionales"""
    try:
        print("🔍 Conectando a PostgreSQL de Railway...")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("✅ Conexión exitosa\n")
            
            # Obtener todos los planes nutricionales
            result = conn.execute(text("""
                SELECT id, user_id, title, meals, created_at
                FROM nutrition_plans
                ORDER BY created_at DESC
                LIMIT 5
            """))
            
            plans = list(result)
            
            if not plans:
                print("⚠️  No hay planes nutricionales en la base de datos")
                return
            
            print(f"📊 Total de planes encontrados: {len(plans)}\n")
            
            for plan in plans:
                print(f"Plan ID: {plan[0]}")
                print(f"  User ID: {plan[1]}")
                print(f"  Título: {plan[2]}")
                print(f"  Meals: {plan[3]}")
                print(f"  Tipo de meals: {type(plan[3])}")
                
                if plan[3]:
                    import json
                    if isinstance(plan[3], str):
                        print("  ⚠️  meals es STRING (debería ser dict/list)")
                        try:
                            parsed = json.loads(plan[3])
                            print(f"  ✅ JSON válido: {len(parsed)} comidas")
                        except:
                            print("  ❌ JSON inválido")
                    elif isinstance(plan[3], (dict, list)):
                        print(f"  ✅ meals es dict/list: {len(plan[3])} comidas")
                    else:
                        print(f"  ❌ meals es tipo desconocido: {type(plan[3])}")
                else:
                    print("  ⚠️  meals es NULL")
                
                print(f"  Creado: {plan[4]}")
                print()
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    check_nutrition_plans()
