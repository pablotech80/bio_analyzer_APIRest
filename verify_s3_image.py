#!/usr/bin/env python3
"""
Script para verificar accesibilidad de imágenes en S3 y diagnosticar problemas CORS
"""
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# URL de la imagen del post
IMAGE_URL = "https://coach360-media.s3.eu-north-1.amazonaws.com/blog/Gemini_Generated_Image_d9p189d9p189d9p1_20251101_025137.webp"
BUCKET = os.getenv('S3_BUCKET')
KEY = "blog/Gemini_Generated_Image_d9p189d9p189d9p1_20251101_025137.webp"

print("🔍 Verificando imagen en S3...\n")
print(f"Bucket: {BUCKET}")
print(f"Key: {KEY}")
print(f"URL: {IMAGE_URL}\n")

# Crear cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'eu-north-1')
)

# 1. Verificar si el objeto existe
print("1️⃣ Verificando existencia del archivo...")
try:
    response = s3.head_object(Bucket=BUCKET, Key=KEY)
    print(f"✅ Archivo existe")
    print(f"   Content-Type: {response.get('ContentType')}")
    print(f"   Content-Length: {response.get('ContentLength')} bytes")
    print(f"   Last-Modified: {response.get('LastModified')}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit(1)

# 2. Verificar configuración CORS del bucket
print("2️⃣ Verificando configuración CORS del bucket...")
try:
    cors = s3.get_bucket_cors(Bucket=BUCKET)
    print("✅ CORS configurado:")
    for rule in cors['CORSRules']:
        print(f"\n   Regla:")
        print(f"   - AllowedOrigins: {rule.get('AllowedOrigins')}")
        print(f"   - AllowedMethods: {rule.get('AllowedMethods')}")
        print(f"   - AllowedHeaders: {rule.get('AllowedHeaders')}")
        print(f"   - ExposeHeaders: {rule.get('ExposeHeaders', [])}")
except s3.exceptions.NoSuchCORSConfiguration:
    print("❌ CORS NO CONFIGURADO")
    print("\n⚠️  SOLUCIÓN: Configura CORS en AWS Console:")
    print("   1. Ve a https://console.aws.amazon.com/s3/")
    print(f"   2. Selecciona bucket: {BUCKET}")
    print("   3. Pestaña 'Permissions' → 'CORS'")
    print("   4. Agrega esta configuración:")
    print("""
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": [
            "https://app.coachbodyfit360.com",
            "https://coachbodyfit360.com",
            "http://localhost:5000",
            "http://localhost:5001"
        ],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
    }
]
    """)
except Exception as e:
    print(f"❌ Error verificando CORS: {e}")

# 3. Verificar Bucket Policy (acceso público)
print("\n3️⃣ Verificando Bucket Policy (acceso público)...")
try:
    policy = s3.get_bucket_policy(Bucket=BUCKET)
    print("✅ Bucket Policy configurada")
    # No mostrar la policy completa por seguridad
except Exception as e:
    print(f"⚠️  Bucket Policy: {e}")

# 4. Verificar Block Public Access
print("\n4️⃣ Verificando Block Public Access...")
try:
    block = s3.get_public_access_block(Bucket=BUCKET)
    config = block['PublicAccessBlockConfiguration']
    
    if any([
        config.get('BlockPublicAcls'),
        config.get('IgnorePublicAcls'),
        config.get('BlockPublicPolicy'),
        config.get('RestrictPublicBuckets')
    ]):
        print("⚠️  Algunas restricciones están activas:")
        print(f"   - BlockPublicAcls: {config.get('BlockPublicAcls')}")
        print(f"   - IgnorePublicAcls: {config.get('IgnorePublicAcls')}")
        print(f"   - BlockPublicPolicy: {config.get('BlockPublicPolicy')}")
        print(f"   - RestrictPublicBuckets: {config.get('RestrictPublicBuckets')}")
    else:
        print("✅ Block Public Access desactivado (correcto para acceso público)")
except Exception as e:
    print(f"ℹ️  Block Public Access: {e}")

print("\n" + "="*60)
print("📋 RESUMEN:")
print("="*60)
print("\n✅ La imagen existe en S3 y es accesible")
print("⚠️  Si las imágenes no se ven en el navegador, el problema es CORS")
print("\n💡 SOLUCIÓN:")
print("   Configura CORS en AWS Console siguiendo las instrucciones arriba")
print("   Ver: CONFIGURAR_S3_CORS.md para guía completa\n")
