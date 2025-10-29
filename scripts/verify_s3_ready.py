#!/usr/bin/env python3
"""
Verificar que S3 está listo para funcionar
"""

import sys

def check_boto3():
    """Verificar que boto3 está instalado"""
    try:
        import boto3
        print("✅ boto3 instalado:", boto3.__version__)
        return True
    except ImportError:
        print("❌ boto3 NO está instalado")
        return False

def check_s3_connection():
    """Verificar conexión a S3"""
    try:
        import boto3
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Verificar variables
        required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'S3_BUCKET', 'AWS_REGION']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            print(f"❌ Variables faltantes: {', '.join(missing)}")
            return False
        
        print("✅ Variables AWS configuradas")
        
        # Probar conexión
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'eu-north-1')
        )
        
        # Listar objetos (solo para verificar conexión)
        bucket = os.getenv('S3_BUCKET')
        s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
        
        print(f"✅ Conexión a S3 exitosa: {bucket}")
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a S3: {e}")
        return False

def main():
    print("🔍 Verificando configuración S3...\n")
    
    results = {
        'boto3': check_boto3(),
        's3_connection': check_s3_connection()
    }
    
    print("\n" + "="*50)
    if all(results.values()):
        print("✅ TODO LISTO - S3 funcionando correctamente")
        print("\n📝 Próximo paso:")
        print("   Crea un análisis con fotos en:")
        print("   https://app.coachbodyfit360.com/bioanalyze/nuevo")
        return 0
    else:
        print("❌ HAY PROBLEMAS - Revisa los errores arriba")
        return 1

if __name__ == "__main__":
    sys.exit(main())
