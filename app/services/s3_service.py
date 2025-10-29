import boto3
import os
import uuid
from flask import current_app


def upload_to_s3(file, folder="biometric_photos"):
    """
    Sube un archivo a Amazon S3 y devuelve su URL
    
    Args:
        file (FileStorage): Archivo de Flask
        folder (str): Carpeta en S3
    
    Returns:
        str: URL pública del archivo
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config.get('AWS_REGION', 'eu-north-1')
    )
    
    # Generar nombre único
    ext = file.filename.split('.')[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"
    
    s3.upload_fileobj(
        file,
        current_app.config['S3_BUCKET'],
        filename,
        ExtraArgs={
            'ContentType': file.content_type,
            'ACL': 'public-read'  # Hacer la foto pública automáticamente
        }
    )
    
    # Construir URL pública con región
    region = current_app.config.get('AWS_REGION', 'eu-north-1')
    return f"https://{current_app.config['S3_BUCKET']}.s3.{region}.amazonaws.com/{filename}"
