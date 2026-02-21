#!/usr/bin/env python3
"""
Script para verificar que el tracking de tokens funciona correctamente.
Ejecutar: python test_token_tracking.py
"""
import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.telegram import LLMUsageLedger
from sqlalchemy import func

def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("VERIFICACIÓN DE TOKEN TRACKING")
        print("=" * 60)
        
        # Obtener estadísticas totales
        total_records = db.session.query(func.count(LLMUsageLedger.id)).scalar()
        total_tokens = db.session.query(func.sum(LLMUsageLedger.total_tokens)).scalar() or 0
        total_cost = db.session.query(func.sum(LLMUsageLedger.cost_usd)).scalar() or 0.0
        
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   Total de registros: {total_records}")
        print(f"   Total de tokens: {total_tokens:,}")
        print(f"   Coste total: ${total_cost:.4f}")
        
        # Por canal
        print(f"\n📡 POR CANAL:")
        channels = db.session.query(
            LLMUsageLedger.channel,
            func.count(LLMUsageLedger.id),
            func.sum(LLMUsageLedger.total_tokens)
        ).group_by(LLMUsageLedger.channel).all()
        
        for channel, count, tokens in channels:
            print(f"   {channel}: {count} registros, {tokens or 0:,} tokens")
        
        # Últimos 5 registros
        print(f"\n🕐 ÚLTIMOS 5 REGISTROS:")
        last_records = LLMUsageLedger.query.order_by(
            LLMUsageLedger.created_at.desc()
        ).limit(5).all()
        
        for record in last_records:
            print(f"   [{record.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                  f"User {record.user_id} | {record.channel} | "
                  f"{record.model_name} | {record.total_tokens} tokens | "
                  f"${record.cost_usd:.6f}")
        
        if not last_records:
            print("   ⚠️  No hay registros en la base de datos")
        
        print("\n" + "=" * 60)
        print("Para probar el tracking:")
        print("1. Envía un mensaje por Telegram al bot")
        print("2. O genera un análisis biométrico desde la web")
        print("3. Ejecuta este script de nuevo para ver los cambios")
        print("=" * 60)

if __name__ == "__main__":
    main()
