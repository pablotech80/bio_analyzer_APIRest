"""
Upload directo a S3 usando presigned URLs
Evita que archivos grandes pasen por el servidor Flask
"""
import os
import boto3
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.blog import blog_bp
from app.utils.decorators import admin_required


@blog_bp.route('/admin/s3/presigned-url', methods=['POST'])
@admin_required
def get_presigned_url():
    """
    Genera una presigned URL para upload directo a S3
    
    El frontend usa esta URL para subir el archivo directamente a S3
    sin pasar por el servidor Flask
    
    Request JSON:
    {
        "filename": "video.mp4",
        "content_type": "video/mp4",
        "file_size": 50000000
    }
    
    Response:
    {
        "success": true,
        "upload_url": "https://s3.amazonaws.com/...",
        "file_url": "https://s3.amazonaws.com/...",
        "fields": {...}
    }
    """
    try:
        data = request.get_json()
        filename = data.get('filename')
        content_type = data.get('content_type')
        file_size = data.get('file_size', 0)
        
        if not filename or not content_type:
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros: filename y content_type'
            }), 400
        
        # Validar tamaño (100MB max)
        max_size = 100 * 1024 * 1024
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': f'Archivo muy grande. Máximo: {max_size / (1024*1024)}MB'
            }), 400
        
        # Configurar S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'eu-north-1')
        )
        
        bucket = os.environ.get('S3_BUCKET') or os.environ.get('AWS_BUCKET_NAME')
        
        # Generar nombre único
        from datetime import datetime
        from werkzeug.utils import secure_filename
        name, ext = os.path.splitext(secure_filename(filename))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"media/{name}_{timestamp}{ext}"
        
        # Generar presigned POST URL (permite upload directo desde navegador)
        # SIN ACL porque el bucket usa Bucket Policy
        presigned_post = s3_client.generate_presigned_post(
            Bucket=bucket,
            Key=unique_filename,
            Fields={
                'Content-Type': content_type
            },
            Conditions=[
                {'Content-Type': content_type},
                ['content-length-range', 0, max_size]
            ],
            ExpiresIn=3600  # 1 hora
        )
        
        # URL final del archivo
        region = os.environ.get('AWS_REGION', 'eu-north-1')
        file_url = f"https://{bucket}.s3.{region}.amazonaws.com/{unique_filename}"
        
        return jsonify({
            'success': True,
            'upload_url': presigned_post['url'],
            'fields': presigned_post['fields'],
            'file_url': file_url,
            'filename': unique_filename
        }), 200
        
    except Exception as e:
        print(f"❌ Error generando presigned URL: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
