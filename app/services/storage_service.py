"""
Servicio de almacenamiento profesional con S3 + CloudFront
Optimización automática de imágenes, generación de thumbnails, CDN
"""
import os
import uuid
from io import BytesIO
from typing import Dict, Optional, Tuple

import boto3
from botocore.exceptions import ClientError
from PIL import Image
from werkzeug.utils import secure_filename


class StorageService:
    """
    Servicio profesional de almacenamiento con AWS S3 + CloudFront
    
    Features:
    - Upload a S3 con optimización automática
    - Conversión a WebP (mejor compresión)
    - Generación de thumbnails
    - URLs de CDN (CloudFront)
    - Manejo robusto de errores
    """
    
    def __init__(self, app=None):
        self.s3_client = None
        self.bucket_name = None
        self.cloudfront_domain = None
        self.region = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar con configuración de Flask"""
        self.bucket_name = app.config.get('S3_BUCKET')
        self.cloudfront_domain = app.config.get('CLOUDFRONT_DOMAIN')
        self.region = app.config.get('AWS_REGION', 'eu-north-1')
        
        # Inicializar cliente S3
        aws_access_key = app.config.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = app.config.get('AWS_SECRET_ACCESS_KEY')
        
        if aws_access_key and aws_secret_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=self.region
            )
    
    def is_configured(self) -> bool:
        """Verifica si S3 está configurado"""
        return (
            self.s3_client is not None and
            self.bucket_name is not None
        )
    
    def upload_image(
        self,
        file,
        folder: str = 'blog',
        optimize: bool = True,
        max_width: int = 1920,
        thumbnail_size: Tuple[int, int] = (400, 400)
    ) -> Dict[str, any]:
        """
        Upload de imagen con optimización automática
        
        Args:
            file: Archivo de imagen (FileStorage de Flask)
            folder: Carpeta en S3 (ej: 'blog', 'profiles', 'analysis')
            optimize: Si True, optimiza y convierte a WebP
            max_width: Ancho máximo de la imagen (mantiene aspect ratio)
            thumbnail_size: Tamaño del thumbnail (ancho, alto)
        
        Returns:
            Dict con:
                - url: URL del CDN (CloudFront)
                - thumbnail_url: URL del thumbnail
                - s3_key: Key en S3
                - size: Tamaño en bytes
                - width: Ancho de la imagen
                - height: Alto de la imagen
        
        Raises:
            Exception: Si falla el upload
        """
        if not self.is_configured():
            raise Exception("S3 no está configurado. Verifica las variables de entorno.")
        
        # Generar nombre único
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_name = f"{name}_{uuid.uuid4().hex[:8]}"
        
        # Leer imagen
        try:
            img = Image.open(file)
            
            # Convertir RGBA a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
        except Exception as e:
            raise Exception(f"Error al leer imagen: {str(e)}")
        
        # Optimizar tamaño
        original_width, original_height = img.size
        if optimize and (img.width > max_width or img.height > max_width):
            img.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)
        
        # Convertir a WebP si optimize=True
        if optimize:
            webp_buffer = BytesIO()
            img.save(webp_buffer, format='WEBP', quality=85, optimize=True)
            webp_buffer.seek(0)
            
            s3_key = f"{folder}/{unique_name}.webp"
            content_type = 'image/webp'
            upload_buffer = webp_buffer
        else:
            # Mantener formato original
            buffer = BytesIO()
            img_format = img.format or 'JPEG'
            img.save(buffer, format=img_format, quality=90)
            buffer.seek(0)
            
            s3_key = f"{folder}/{unique_name}{ext}"
            content_type = f'image/{img_format.lower()}'
            upload_buffer = buffer
        
        # Upload a S3
        try:
            self.s3_client.upload_fileobj(
                upload_buffer,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'max-age=31536000',  # 1 año
                    'ACL': 'public-read'
                }
            )
        except ClientError as e:
            raise Exception(f"Error al subir a S3: {str(e)}")
        
        # Generar thumbnail
        thumb_key = None
        thumb_url = None
        if thumbnail_size:
            try:
                thumb_key = self._create_thumbnail(
                    img,
                    f"{folder}/thumbs",
                    unique_name,
                    thumbnail_size
                )
                thumb_url = self._get_cdn_url(thumb_key)
            except Exception as e:
                print(f"⚠️  Warning: No se pudo crear thumbnail: {e}")
        
        # URL del CDN
        cdn_url = self._get_cdn_url(s3_key)
        
        return {
            'url': cdn_url,
            'thumbnail_url': thumb_url,
            's3_key': s3_key,
            'size': upload_buffer.tell(),
            'width': img.width,
            'height': img.height,
            'original_width': original_width,
            'original_height': original_height
        }
    
    def _create_thumbnail(
        self,
        img: Image.Image,
        folder: str,
        name: str,
        size: Tuple[int, int]
    ) -> str:
        """
        Crear thumbnail de una imagen
        
        Args:
            img: Imagen PIL
            folder: Carpeta en S3
            name: Nombre base del archivo
            size: Tupla (ancho, alto)
        
        Returns:
            S3 key del thumbnail
        """
        thumb = img.copy()
        thumb.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_buffer = BytesIO()
        thumb.save(thumb_buffer, format='WEBP', quality=80, optimize=True)
        thumb_buffer.seek(0)
        
        thumb_key = f"{folder}/{name}_thumb.webp"
        
        self.s3_client.upload_fileobj(
            thumb_buffer,
            self.bucket_name,
            thumb_key,
            ExtraArgs={
                'ContentType': 'image/webp',
                'CacheControl': 'max-age=31536000',
                'ACL': 'public-read'
            }
        )
        
        return thumb_key
    
    def _get_cdn_url(self, s3_key: str) -> str:
        """
        Genera URL del CDN (CloudFront) o S3 directo
        
        Args:
            s3_key: Key del archivo en S3
        
        Returns:
            URL completa del archivo
        """
        if self.cloudfront_domain:
            # Usar CloudFront (CDN)
            return f"https://{self.cloudfront_domain}/{s3_key}"
        else:
            # Usar S3 directo (sin CDN)
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
    
    def delete_file(self, s3_key: str) -> bool:
        """
        Eliminar archivo de S3
        
        Args:
            s3_key: Key del archivo en S3
        
        Returns:
            True si se eliminó correctamente
        """
        if not self.is_configured():
            raise Exception("S3 no está configurado")
        
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            print(f"Error al eliminar archivo: {e}")
            return False
    
    def upload_file(
        self,
        file,
        folder: str = 'uploads',
        allowed_extensions: Optional[set] = None
    ) -> Dict[str, any]:
        """
        Upload genérico de archivos (videos, audios, PDFs, etc.)
        
        Args:
            file: Archivo (FileStorage de Flask)
            folder: Carpeta en S3
            allowed_extensions: Set de extensiones permitidas (ej: {'mp4', 'mov'})
        
        Returns:
            Dict con url, s3_key, size, mime_type
        """
        if not self.is_configured():
            raise Exception("S3 no está configurado")
        
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        
        # Verificar extensión
        if allowed_extensions:
            if ext.lower().lstrip('.') not in allowed_extensions:
                raise Exception(f"Extensión no permitida: {ext}")
        
        # Generar nombre único
        unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        s3_key = f"{folder}/{unique_name}"
        
        # Detectar MIME type
        mime_type = file.content_type or 'application/octet-stream'
        
        # Upload a S3
        try:
            file.seek(0)  # Asegurar que estamos al inicio del archivo
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': mime_type,
                    'CacheControl': 'max-age=31536000',
                    'ACL': 'public-read'
                }
            )
        except ClientError as e:
            raise Exception(f"Error al subir archivo: {str(e)}")
        
        # Obtener tamaño
        file.seek(0, 2)  # Ir al final
        file_size = file.tell()
        file.seek(0)  # Volver al inicio
        
        return {
            'url': self._get_cdn_url(s3_key),
            's3_key': s3_key,
            'size': file_size,
            'mime_type': mime_type,
            'filename': unique_name
        }


# Instancia global (se inicializa en create_app)
storage_service = StorageService()
