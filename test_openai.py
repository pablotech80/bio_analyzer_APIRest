#!/usr/bin/env python3
"""
Script para probar la conexión con OpenAI API
"""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

def test_openai_connection():
    """Probar conexión con OpenAI"""
    print("=" * 60)
    print("TEST DE CONEXIÓN OPENAI - FITMASTER")
    print("=" * 60)
    
    # 1. Verificar API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    print(f"   Longitud: {len(api_key)} caracteres")
    
    # 2. Inicializar cliente
    try:
        print("\n🔄 Inicializando cliente OpenAI...")
        client = OpenAI(api_key=api_key)
        print("✅ Cliente inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar cliente: {e}")
        return False
    
    # 3. Probar conexión con una solicitud simple
    try:
        print("\n🔄 Probando conexión con API...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de prueba."},
                {"role": "user", "content": "Di 'Conexión exitosa' si me recibes."}
            ],
            max_tokens=50
        )
        
        respuesta = response.choices[0].message.content
        print(f"✅ Respuesta recibida: {respuesta}")
        print(f"   Modelo usado: {response.model}")
        print(f"   Tokens usados: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"❌ Error en la solicitud: {e}")
        return False
    
    # 4. Probar con datos biométricos simulados
    try:
        print("\n🔄 Probando análisis FitMaster...")
        test_data = {
            "weight": 75,
            "height": 175,
            "age": 30,
            "gender": "male",
            "bmi": 24.5,
            "body_fat_percentage": 18,
            "goal": "Ganancia muscular"
        }
        
        prompt = f"""Analiza estos datos biométricos:
Peso: {test_data['weight']}kg
Altura: {test_data['height']}cm
Edad: {test_data['age']} años
IMC: {test_data['bmi']}
Grasa corporal: {test_data['body_fat_percentage']}%
Objetivo: {test_data['goal']}

Responde en JSON con: interpretation, nutrition_plan, training_plan"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres FitMaster, experto en fitness."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        fitmaster_response = response.choices[0].message.content
        print(f"✅ FitMaster respondió ({len(fitmaster_response)} caracteres)")
        print(f"   Primeros 200 caracteres: {fitmaster_response[:200]}...")
        
    except Exception as e:
        print(f"❌ Error en análisis FitMaster: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_openai_connection()
    sys.exit(0 if success else 1)
