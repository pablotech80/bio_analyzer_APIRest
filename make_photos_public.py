#!/usr/bin/env python3
"""
Script para hacer públicas las fotos existentes en S3
"""
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

def make_photos_public():
    """Hace públicas todas las fotos en el bucket S3"""
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'eu-north-1')
    )
    
    bucket = os.getenv('S3_BUCKET')
    
    print(f"🔓 Haciendo públicas las fotos en bucket '{bucket}'...\n")
    
    try:
        # Listar todas las fotos
        response = s3.list_objects_v2(Bucket=bucket, Prefix='biometric_photos/')
        
        if 'Contents' not in response:
            print("❌ No se encontraron fotos")
            return
        
        for obj in response['Contents']:
            key = obj['Key']
            print(f"  📁 {key}")
            
            # Cambiar ACL a public-read
            s3.put_object_acl(
                Bucket=bucket,
                Key=key,
                ACL='public-read'
            )
            print(f"     ✅ Ahora es pública")
            print(f"     🔗 https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}\n")
        
        print(f"✅ {len(response['Contents'])} fotos ahora son públicas")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    make_photos_public()
