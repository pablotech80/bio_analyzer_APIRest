"""
Migración para crear tabla media_files
"""
from app import create_app, db
from app.models.media_file import MediaFile

def run_migration():
    """Ejecuta la migración"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creando tabla media_files...")
        
        # Crear tabla
        db.create_all()
        
        print("✅ Tabla media_files creada exitosamente!")
        print("\n📊 Estructura de la tabla:")
        print("  - id (PK)")
        print("  - filename, file_path (unique), file_url")
        print("  - file_type (image/video/audio), mime_type, file_size")
        print("  - title, alt_text, caption (metadata)")
        print("  - width, height (para imágenes/videos)")
        print("  - duration (para videos/audios)")
        print("  - uploaded_by (FK a users)")
        print("  - usage_count, uploaded_at")
        print("\n🎯 Índices creados en: uploaded_at")
        print("\n📁 Tipos de archivos soportados:")
        print("  - Imágenes: JPG, PNG, GIF, WebP")
        print("  - Videos: MP4, WebM")
        print("  - Audios: MP3, WAV, OGG (NotebookLM)")

if __name__ == '__main__':
    run_migration()
