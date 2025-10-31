"""
Migración para crear tabla blog_posts
"""
from app import create_app, db
from app.models.blog_post import BlogPost

def run_migration():
    """Ejecuta la migración"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creando tabla blog_posts...")
        
        # Crear tabla
        db.create_all()
        
        print("✅ Tabla blog_posts creada exitosamente!")
        print("\n📊 Estructura de la tabla:")
        print("  - id (PK)")
        print("  - title, slug (unique), excerpt, content (Markdown)")
        print("  - featured_image")
        print("  - category, tags")
        print("  - meta_description, meta_keywords (SEO)")
        print("  - author_id (FK a users)")
        print("  - is_published, published_at")
        print("  - views_count, reading_time")
        print("  - created_at, updated_at")
        print("\n🎯 Índices creados en: slug, category, published_at")

if __name__ == '__main__':
    run_migration()
