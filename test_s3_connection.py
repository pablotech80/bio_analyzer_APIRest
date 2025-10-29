#!/usr/bin/env python3
"""
Script para probar la conexión con AWS S3
Verifica que las credenciales y el bucket estén correctamente configurados
"""
import os
import sys
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Cargar variables de entorno
load_dotenv()

def test_s3_connection():
    """Prueba la conexión con S3 y lista los buckets disponibles"""
    
    print("🔍 Verificando configuración AWS S3...\n")
    
    # Verificar variables de entorno
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3_bucket = os.getenv('S3_BUCKET')
    aws_region = os.getenv('AWS_REGION', 'eu-north-1')
    
    if not aws_access_key:
        print("❌ AWS_ACCESS_KEY_ID no configurado en .env")
        return False
    
    if not aws_secret_key:
        print("❌ AWS_SECRET_ACCESS_KEY no configurado en .env")
        return False
    
    if not s3_bucket:
        print("❌ S3_BUCKET no configurado en .env")
        return False
    
    print(f"✅ AWS_ACCESS_KEY_ID: {aws_access_key[:10]}...")
    print(f"✅ S3_BUCKET: {s3_bucket}")
    print(f"✅ AWS_REGION: {aws_region}\n")
    
    try:
        # Crear cliente S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        print("🔗 Conectando con AWS S3...")
        
        # Listar buckets disponibles
        response = s3_client.list_buckets()
        print(f"\n✅ Conexión exitosa! Buckets disponibles:")
        for bucket in response['Buckets']:
            marker = "👉" if bucket['Name'] == s3_bucket else "  "
            print(f"{marker} - {bucket['Name']}")
        
        # Verificar que el bucket configurado existe
        if s3_bucket not in [b['Name'] for b in response['Buckets']]:
            print(f"\n⚠️  ADVERTENCIA: El bucket '{s3_bucket}' no existe en tu cuenta AWS")
            print(f"   Crea el bucket o actualiza S3_BUCKET en .env")
            return False
        
        # Verificar permisos en el bucket
        print(f"\n🔐 Verificando permisos en bucket '{s3_bucket}'...")
        try:
            s3_client.head_bucket(Bucket=s3_bucket)
            print(f"✅ Tienes acceso al bucket '{s3_bucket}'")
            
            # Intentar listar objetos (sin crear nada)
            response = s3_client.list_objects_v2(Bucket=s3_bucket, MaxKeys=1)
            print(f"✅ Permisos de lectura: OK")
            
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '403':
                print(f"❌ Sin permisos para acceder al bucket '{s3_bucket}'")
                print("   Verifica la política IAM del usuario")
            elif error_code == '404':
                print(f"❌ El bucket '{s3_bucket}' no existe")
            else:
                print(f"❌ Error: {e}")
            return False
            
    except NoCredentialsError:
        print("❌ Credenciales AWS no válidas")
        return False
    except ClientError as e:
        print(f"❌ Error de cliente AWS: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST DE CONEXIÓN AWS S3 - CoachBodyFit360")
    print("=" * 60 + "\n")
    
    success = test_s3_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ CONFIGURACIÓN CORRECTA - Listo para subir fotos")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ CONFIGURACIÓN INCORRECTA - Revisa los errores arriba")
        print("=" * 60)
        sys.exit(1)
