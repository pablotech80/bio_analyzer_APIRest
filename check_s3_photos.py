#!/usr/bin/env python3
"""
Script para verificar las fotos subidas a S3
"""
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

def list_s3_photos():
    """Lista todas las fotos en el bucket S3"""
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'eu-north-1')
    )
    
    bucket = os.getenv('S3_BUCKET')
    
    print(f"📸 Fotos en bucket '{bucket}':\n")
    
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix='biometric_photos/')
        
        if 'Contents' in response:
            print(f"✅ Encontradas {len(response['Contents'])} fotos:\n")
            for obj in response['Contents']:
                size_kb = obj['Size'] / 1024
                print(f"  📁 {obj['Key']}")
                print(f"     Tamaño: {size_kb:.2f} KB")
                print(f"     Fecha: {obj['LastModified']}")
                print(f"     URL: https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{obj['Key']}\n")
        else:
            print("❌ No se encontraron fotos en el bucket")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_s3_photos()
