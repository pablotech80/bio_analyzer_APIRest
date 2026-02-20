# app/services/storage_service.py
"""
Servicio de almacenamiento de archivos
Soporta: Local filesystem y S3
Maneja correctamente FileStorage con PIL
"""
import os
import io
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import boto3
from botocore.exceptions import ClientError


class StorageService:
    """
    Servicio de almacenamiento de archivos

    Features:
    - Upload a filesystem local
    - Upload a S3 (si está configurado)
    - Optimización automática de imágenes
    - Generación de thumbnails
    - Conversión a WebP
    """

    def __init__(self, flask_app=None):
        self.s3_client = None
        self.s3_bucket = None
        self.cloudfront_domain = None
        self.use_s3 = False
        self.upload_folder = None

        if flask_app:
            self.init_app(flask_app)

    def init_app(self, flask_app):
        """Inicializar con configuración de Flask"""
        # S3 Configuration

        aws_bucket = os.environ.get('S3_BUCKET') or os.environ.get('AWS_BUCKET_NAME')
        aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION', 'eu-north-1')

        if aws_bucket and aws_key and aws_secret:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret,
                    region_name=aws_region
                    )
                self.s3_bucket = aws_bucket
                self.cloudfront_domain = os.environ.get('CLOUDFRONT_DOMAIN')
                self.use_s3 = True
                print(f"✅ S3 configurado: bucket={aws_bucket}, region={aws_region}")
            except Exception as e:
                print(f"⚠️ Error configurando S3: {e}")
                self.use_s3 = False
        else:
            print("ℹ️ S3 no configurado, usando almacenamiento local")
            self.use_s3 = False

        # Local storage fallback
        self.upload_folder = flask_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(self.upload_folder, exist_ok=True)

    def save_file(self, file):
        """
        Guarda archivo (imagen, video o audio)

        Args:
            file: FileStorage object de Flask

        Returns:
            dict con información del archivo guardado
        """
        print("\n=== INICIO SAVE_FILE ===")
        print(f"Archivo: {file.filename}")
        print(f"Content-Type: {file.content_type}")
        print(f"S3 habilitado: {self.use_s3}")

        # Generar nombre seguro
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{name}_{timestamp}{ext}"

        # Detectar tipo de archivo
        file_type = self._detect_file_type(file.content_type)

        # Procesar según tipo
        if file_type == 'image':
            return self._save_image(file, unique_filename)
        elif file_type == 'video':
            return self._save_video(file, unique_filename)
        elif file_type == 'audio':
            return self._save_audio(file, unique_filename)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file.content_type}")

    def _save_image(self, file, filename):
        """
        Guarda imagen con optimización

        IMPORTANTE: Maneja correctamente el FileStorage para evitar
        "I/O operation on closed file"
        """
        print("\n=== PROCESANDO IMAGEN ===")

        # 1. LEER EL ARCHIVO COMPLETO A MEMORIA
        # Esto evita que PIL cierre el FileStorage
        file_data = file.read()
        file_size = len(file_data)
        print(f"Archivo leído: {file_size} bytes")

        # 2. PROCESAR IMAGEN CON PIL
        # Usar BytesIO para mantener los datos en memoria
        img_buffer = io.BytesIO(file_data)
        img = Image.open(img_buffer)

        # Obtener dimensiones originales
        width, height = img.size
        print(f"Dimensiones: {width}x{height}, modo: {img.mode}")

        # 3. OPTIMIZAR IMAGEN
        # Convertir a RGB si es necesario (para WebP)
        if img.mode in ('RGBA', 'P'):
            # Crear fondo blanco para transparencias
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])  # Usar alpha channel como mask
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Redimensionar si es muy grande (opcional)
        max_size = 2048
        if width > max_size or height > max_size:
            print(f"Redimensionando de {width}x{height} a max {max_size}")
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            width, height = img.size

        # 4. GUARDAR EN FORMATO OPTIMIZADO
        # Convertir a WebP para mejor compresión
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='WEBP', quality=85, optimize=True)
        output_buffer.seek(0)

        # Cambiar extensión a .webp
        name, ext = os.path.splitext(filename)
        webp_filename = f"{name}.webp"

        print(f"Imagen optimizada: {len(output_buffer.getvalue())} bytes")

        # 5. SUBIR A S3 O GUARDAR LOCALMENTE
        if self.use_s3:
            return self._upload_to_s3(
                output_buffer,
                webp_filename,
                'image/webp',
                width,
                height
                )
        else:
            return self._save_to_local(
                output_buffer,
                webp_filename,
                'image/webp',
                width,
                height
                )

    def _save_video(self, file, filename):
        """Guarda video sin procesamiento"""
        print("\n=== PROCESANDO VIDEO ===")

        # Leer archivo completo
        file_data = file.read()
        file_size = len(file_data)
        print(f"Video leído: {file_size} bytes")

        # Crear buffer
        video_buffer = io.BytesIO(file_data)

        if self.use_s3:
            return self._upload_to_s3(
                video_buffer,
                filename,
                file.content_type or 'video/mp4'
                )
        else:
            return self._save_to_local(
                video_buffer,
                filename,
                file.content_type or 'video/mp4'
                )

    def _save_audio(self, file, filename):
        """Guarda audio sin procesamiento"""
        print("\n=== PROCESANDO AUDIO ===")

        # Leer archivo completo
        file_data = file.read()
        file_size = len(file_data)
        print(f"Audio leído: {file_size} bytes")

        # Crear buffer
        audio_buffer = io.BytesIO(file_data)

        if self.use_s3:
            return self._upload_to_s3(
                audio_buffer,
                filename,
                file.content_type or 'audio/mpeg'
                )
        else:
            return self._save_to_local(
                audio_buffer,
                filename,
                file.content_type or 'audio/mpeg'
                )

    def _upload_to_s3(self, file_buffer, filename, content_type, width=None, height=None):
        """
        Sube archivo a S3

        Args:
            file_buffer: BytesIO con el contenido del archivo
            filename: Nombre del archivo
            content_type: MIME type
            width, height: Dimensiones (opcional, para imágenes)
        """
        print("\n=== UPLOAD A S3 ===")
        print(f"Bucket: {self.s3_bucket}")
        print(f"Filename: {filename}")
        print(f"Content-Type: {content_type}")

        try:
            # Construir key de S3
            folder = 'blog' if 'image' in content_type else 'media'
            s3_key = f"{folder}/{filename}"

            # Obtener tamaño ANTES del upload
            file_buffer.seek(0, 2)  # Ir al final
            file_size = file_buffer.tell()
            file_buffer.seek(0)  # Volver al inicio

            # Upload a S3
            self.s3_client.upload_fileobj(
                file_buffer,
                self.s3_bucket,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'max-age=31536000'  # 1 año
                    }
                )

            # Construir URL
            if self.cloudfront_domain:
                file_url = f"https://{self.cloudfront_domain}/{s3_key}"
            else:
                region = os.environ.get('AWS_REGION', 'eu-north-1')
                file_url = f"https://{self.s3_bucket}.s3.{region}.amazonaws.com/{s3_key}"

            print(f"✅ Archivo subido: {file_url}")

            return {
                'filename': filename,
                'file_path': s3_key,
                'file_url': file_url,
                'file_type': self._detect_file_type(content_type),
                'mime_type': content_type,
                'file_size': file_size,
                'width': width,
                'height': height,
                'storage': 's3'
                }

        except ClientError as e:
            print(f"❌ Error en S3: {e}")
            raise Exception(f"Error al subir a S3: {str(e)}")

    def _save_to_local(self, file_buffer, filename, content_type, width=None, height=None):
        """
        Guarda archivo localmente

        Args:
            file_buffer: BytesIO con el contenido del archivo
            filename: Nombre del archivo
            content_type: MIME type
            width, height: Dimensiones (opcional, para imágenes)
        """
        print("\n=== GUARDANDO LOCALMENTE ===")

        # Crear subcarpeta según tipo
        folder = 'images' if 'image' in content_type else 'media'
        full_folder = os.path.join(self.upload_folder, folder)
        os.makedirs(full_folder, exist_ok=True)

        # Ruta completa
        file_path = os.path.join(full_folder, filename)

        # Guardar archivo
        with open(file_path, 'wb') as f:
            f.write(file_buffer.getvalue())

        # URL relativa
        file_url = f"/uploads/{folder}/{filename}"

        print(f"✅ Archivo guardado: {file_path}")

        return {
            'filename': filename,
            'file_path': file_path,
            'file_url': file_url,
            'file_type': self._detect_file_type(content_type),
            'mime_type': content_type,
            'file_size': os.path.getsize(file_path),
            'width': width,
            'height': height,
            'storage': 'local'
            }

    def _detect_file_type(self, content_type):
        """Detecta el tipo de archivo según MIME type"""
        if content_type.startswith('image/'):
            return 'image'
        elif content_type.startswith('video/'):
            return 'video'
        elif content_type.startswith('audio/'):
            return 'audio'
        else:
            return 'other'

    def delete_file(self, file_path, storage='local'):
        """
        Elimina un archivo

        Args:
            file_path: Ruta del archivo (local o S3 key)
            storage: 'local' o 's3'
        """
        try:
            if storage == 's3' and self.use_s3:
                self.s3_client.delete_object(
                    Bucket=self.s3_bucket,
                    Key=file_path
                    )
                print(f"✅ Archivo eliminado de S3: {file_path}")
            else:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"✅ Archivo eliminado localmente: {file_path}")

        except Exception as e:
            print(f"❌ Error al eliminar archivo: {e}")
            raise


# ============================================================================
# INSTANCIA GLOBAL (Singleton)
# ============================================================================
_storage_service = None


def get_storage_service(flask_app=None):
    """
    Obtiene la instancia del servicio de almacenamiento

    Uso:
        storage = get_storage_service(flask_app)
        file_info = storage.save_file(file)
    """
    global _storage_service

    if _storage_service is None and flask_app:
        _storage_service = StorageService(flask_app)

    return _storage_service