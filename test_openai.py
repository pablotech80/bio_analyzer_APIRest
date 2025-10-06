#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de OpenAI
"""
import os
import sys

def test_openai_setup():
    """Diagnosticar la configuración de OpenAI"""
    print("🔍 Diagnóstico de OpenAI Setup")
    print("=" * 40)
    
    # 1. Verificar si openai está instalado
    try:
        import openai
        print("✅ Dependencia 'openai' instalada correctamente")
        print(f"   Versión: {openai.__version__}")
    except ImportError:
        print("❌ Dependencia 'openai' NO está instalada")
        print("   Solución: pip install openai==1.51.2")
        return False
    
    # 2. Verificar variable de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no está configurada")
        print("   Solución: Agregar OPENAI_API_KEY a tu archivo .env")
        return False
    
    print("✅ OPENAI_API_KEY está configurada")
    print(f"   Key (primeros 10 caracteres): {api_key[:10]}...")
    
    # 3. Intentar inicializar cliente con inicialización simple
    try:
        from openai import OpenAI
        # Inicialización simple sin argumentos adicionales
        client = OpenAI(api_key=api_key)
        print("✅ Cliente OpenAI inicializado correctamente")
        
        # 4. Test básico de modelos disponibles (sin costo)
        try:
            print("🔄 Probando conexión básica...")
            models = client.models.list()
            print("✅ Conexión con OpenAI exitosa")
            print(f"   Modelos disponibles: {len(list(models.data))} encontrados")
        except Exception as e:
            print(f"⚠️  Conexión básica falló: {e}")
            print("   Esto puede ser normal si hay restricciones de red")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar cliente OpenAI: {e}")
        print("   Posibles soluciones:")
        print("   - Verificar que la API key sea válida")
        print("   - Actualizar la librería: pip install --upgrade openai")
        return False

def main():
    """Función principal"""
    # Cargar variables de entorno desde .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Variables de entorno cargadas desde .env")
    except ImportError:
        print("⚠️  python-dotenv no disponible, usando variables de sistema")
    
    success = test_openai_setup()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ¡Configuración de OpenAI correcta!")
        print("   Tu FitMasterService debería funcionar ahora.")
        print("\n🔧 Próximos pasos:")
        print("   1. Asegúrate de que fitmaster_service.py use inicialización simple")
        print("   2. Reinicia tu aplicación Flask")
        print("   3. Prueba un análisis biométrico")
    else:
        print("🚨 Hay problemas con la configuración de OpenAI")
        print("   Revisa los errores arriba y sigue las soluciones.")
        print("\n🔧 Próximos pasos:")
        print("   1. Corrige los problemas identificados")
        print("   2. Ejecuta este script nuevamente")
        print("   3. Reinicia tu aplicación Flask")

if __name__ == "__main__":
    main()
