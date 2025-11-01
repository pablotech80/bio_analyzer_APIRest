#!/usr/bin/env python3
"""
Script para probar el StorageService
Verifica que el servicio está correctamente inicializado
"""
import sys
from app import create_app
from app.services.storage_service import storage_service

print("=" * 70)
print("  TEST DE STORAGE SERVICE - CoachBodyFit360")
print("=" * 70 + "\n")

# Crear app
print("🏗️  Creando aplicación Flask...")
app = create_app('development')

with app.app_context():
    print("✅ App creada\n")
    
    # Verificar configuración
    print("🔍 Verificando configuración...")
    print(f"   S3_BUCKET: {app.config.get('S3_BUCKET')}")
    print(f"   AWS_REGION: {app.config.get('AWS_REGION')}")
    print(f"   AWS_ACCESS_KEY_ID: {app.config.get('AWS_ACCESS_KEY_ID')[:10]}...")
    print()
    
    # Verificar StorageService
    print("🔍 Verificando StorageService...")
    print(f"   Bucket configurado: {storage_service.bucket_name}")
    print(f"   Región: {storage_service.region}")
    print(f"   Cliente S3: {'✅ Inicializado' if storage_service.s3_client else '❌ No inicializado'}")
    print(f"   CloudFront: {storage_service.cloudfront_domain or 'No configurado (usará S3 directo)'}")
    print()
    
    # Verificar si está configurado
    if storage_service.is_configured():
        print("✅ StorageService está correctamente configurado")
        print()
        print("🎉 ¡Listo para subir imágenes a S3!")
        print()
        print("Próximos pasos:")
        print("1. Actualizar rutas de upload del blog para usar storage_service")
        print("2. Probar upload de imagen desde el admin del blog")
        print("3. Verificar que la imagen se sube a S3")
        sys.exit(0)
    else:
        print("❌ StorageService NO está configurado")
        print()
        print("Posibles causas:")
        print("- Faltan credenciales AWS en .env")
        print("- El servicio no se inicializó correctamente")
        sys.exit(1)

print("\n" + "=" * 70)
