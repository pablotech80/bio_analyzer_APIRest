#!/usr/bin/env python3
"""
Script para probar la conexión OpenAI en producción
Simula el entorno de Railway
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_openai_connection():
    """Probar conexión OpenAI con la API Key actual"""
    
    print("=" * 60)
    print("TEST DE OPENAI - SIMULANDO PRODUCCIÓN")
    print("=" * 60)
    
    # Verificar API Key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no encontrada")
        print("   Ejecuta: export OPENAI_API_KEY='tu-api-key'")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    print(f"   Longitud: {len(api_key)} caracteres")
    print()
    
    # Verificar formato
    if not api_key.startswith('sk-'):
        print("⚠️  ADVERTENCIA: La API Key no empieza con 'sk-'")
        print("   Formato esperado: sk-proj-... o sk-...")
        print()
    
    # Probar conexión
    try:
        from openai import OpenAI
        
        print("🔄 Inicializando cliente OpenAI...")
        client = OpenAI(api_key=api_key)
        
        print("🔄 Probando conexión con API...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Responde brevemente."},
                {"role": "user", "content": "Di 'OK' si funciona"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ Respuesta recibida: {result}")
        print(f"   Modelo: {response.model}")
        print(f"   Tokens: {response.usage.total_tokens}")
        print()
        
        print("=" * 60)
        print("✅ CONEXIÓN EXITOSA - API KEY VÁLIDA")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        
        if "401" in str(e) or "invalid_api_key" in str(e):
            print("🔍 DIAGNÓSTICO:")
            print("   - La API Key es inválida o expirada")
            print("   - Verifica en: https://platform.openai.com/api-keys")
            print("   - Genera una nueva key si es necesario")
        elif "429" in str(e):
            print("🔍 DIAGNÓSTICO:")
            print("   - Límite de rate alcanzado")
            print("   - Espera unos minutos e intenta de nuevo")
        elif "insufficient_quota" in str(e):
            print("🔍 DIAGNÓSTICO:")
            print("   - Sin créditos en la cuenta OpenAI")
            print("   - Agrega créditos en: https://platform.openai.com/account/billing")
        
        print()
        print("=" * 60)
        print("❌ CONEXIÓN FALLIDA")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_openai_connection()
