"""
Utilidades para upload de archivos multimedia
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import mimetypes

# Configuración
UPLOAD_FOLDER = 'app/static/uploads/blog'
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'video': {'mp4', 'webm', 'mov'},
    'audio': {'mp3', 'wav', 'ogg', 'm4a'}
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def allowed_file(filename, file_type=None):
    """
    Verifica si el archivo tiene una extensión permitida
    
    Args:
        filename (str): Nombre del archivo
        file_type (str): Tipo de archivo (image, video, audio)
        
    Returns:
        bool: True si está permitido
    """
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type:
        return ext in ALLOWED_EXTENSIONS.get(file_type, set())
    
    # Verificar en todos los tipos
    all_extensions = set()
    for extensions in ALLOWED_EXTENSIONS.values():
        all_extensions.update(extensions)
    
    return ext in all_extensions


def get_file_type(filename):
    """
    Determina el tipo de archivo basado en la extensión
    
    Args:
        filename (str): Nombre del archivo
        
    Returns:
        str: Tipo de archivo (image, video, audio) o None
    """
    if '.' not in filename:
        return None
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    
    return None


def generate_unique_filename(filename):
    """
    Genera un nombre de archivo único
    
    Args:
        filename (str): Nombre original del archivo
        
    Returns:
        str: Nombre único del archivo
    """
    # Obtener extensión
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Generar nombre único
    unique_id = uuid.uuid4().hex[:12]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return f"{timestamp}_{unique_id}.{ext}"


def save_uploaded_file(file, file_type=None):
    """
    Guarda un archivo subido y retorna información
    
    Args:
        file: Archivo de werkzeug
        file_type (str): Tipo de archivo (opcional)
        
    Returns:
        dict: Información del archivo guardado
    """
    if not file or not file.filename:
        raise ValueError("No se proporcionó ningún archivo")
    
    # Verificar extensión
    if not allowed_file(file.filename, file_type):
        raise ValueError(f"Tipo de archivo no permitido: {file.filename}")
    
    # Determinar tipo de archivo
    detected_type = get_file_type(file.filename)
    if not detected_type:
        raise ValueError("No se pudo determinar el tipo de archivo")
    
    # Generar nombre único
    unique_filename = generate_unique_filename(file.filename)
    
    # Determinar carpeta según tipo
    subfolder = f"{detected_type}s"  # images, videos, audios
    upload_path = os.path.join(UPLOAD_FOLDER, subfolder)
    
    # Crear directorio si no existe
    os.makedirs(upload_path, exist_ok=True)
    
    # Ruta completa del archivo
    file_path = os.path.join(upload_path, unique_filename)
    
    # Guardar archivo
    file.save(file_path)
    
    # Obtener información del archivo
    file_size = os.path.getsize(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    
    # URL pública
    file_url = f"/static/uploads/blog/{subfolder}/{unique_filename}"
    
    # Información adicional según tipo
    width = height = duration = None
    
    if detected_type == 'image':
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Optimizar imagen si es muy grande
                if width > 1920 or height > 1920:
                    img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                    img.save(file_path, optimize=True, quality=85)
                    file_size = os.path.getsize(file_path)
        except Exception as e:
            print(f"Error procesando imagen: {e}")
    
    return {
        'filename': file.filename,
        'unique_filename': unique_filename,
        'file_path': file_path,
        'file_url': file_url,
        'file_type': detected_type,
        'mime_type': mime_type,
        'file_size': file_size,
        'width': width,
        'height': height,
        'duration': duration
    }


def delete_file(file_path):
    """
    Elimina un archivo del sistema
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        bool: True si se eliminó correctamente
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error eliminando archivo: {e}")
        return False
