#!/usr/bin/env python3
"""
Script para crear las tablas del blog en producción
Ejecutar: python create_blog_tables.py
"""
import os
from app import create_app, db
from sqlalchemy import text, inspect

def create_blog_tables():
    """Crea las tablas media_files y blog_posts si no existen"""
    
    # Forzar ambiente de producción
    os.environ['FLASK_ENV'] = 'production'
    
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print("="*60)
        print("CREANDO TABLAS DEL BLOG EN PRODUCCIÓN")
        print("="*60)
        print(f"\nTablas existentes: {existing_tables}")
        
        # SQL para crear media_files
        media_files_sql = """
        CREATE TABLE IF NOT EXISTS media_files (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_url VARCHAR(500) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            mime_type VARCHAR(100),
            file_size INTEGER,
            title VARCHAR(200),
            alt_text VARCHAR(200),
            caption VARCHAR(500),
            width INTEGER,
            height INTEGER,
            duration INTEGER,
            uploaded_by INTEGER NOT NULL REFERENCES users(id),
            usage_count INTEGER DEFAULT 0,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE UNIQUE INDEX IF NOT EXISTS ix_media_files_file_path ON media_files(file_path);
        CREATE INDEX IF NOT EXISTS ix_media_files_uploaded_at ON media_files(uploaded_at);
        """
        
        # SQL para crear blog_posts
        blog_posts_sql = """
        CREATE TABLE IF NOT EXISTS blog_posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            slug VARCHAR(250) NOT NULL,
            excerpt VARCHAR(300),
            content TEXT NOT NULL,
            featured_image VARCHAR(500),
            category VARCHAR(50),
            tags VARCHAR(200),
            meta_description VARCHAR(160),
            meta_keywords VARCHAR(200),
            author_id INTEGER NOT NULL REFERENCES users(id),
            is_published BOOLEAN DEFAULT TRUE,
            published_at TIMESTAMP,
            views_count INTEGER DEFAULT 0,
            reading_time INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE UNIQUE INDEX IF NOT EXISTS ix_blog_posts_slug ON blog_posts(slug);
        CREATE INDEX IF NOT EXISTS ix_blog_posts_category ON blog_posts(category);
        CREATE INDEX IF NOT EXISTS ix_blog_posts_published_at ON blog_posts(published_at);
        """
        
        try:
            # Crear media_files
            if 'media_files' not in existing_tables:
                print("\n📊 Creando tabla media_files...")
                db.session.execute(text(media_files_sql))
                db.session.commit()
                print("✅ Tabla media_files creada")
            else:
                print("\n✅ Tabla media_files ya existe")
            
            # Crear blog_posts
            if 'blog_posts' not in existing_tables:
                print("\n📊 Creando tabla blog_posts...")
                db.session.execute(text(blog_posts_sql))
                db.session.commit()
                print("✅ Tabla blog_posts creada")
            else:
                print("\n✅ Tabla blog_posts ya existe")
            
            # Verificar tablas creadas
            inspector = inspect(db.engine)
            final_tables = inspector.get_table_names()
            print(f"\n📋 Tablas finales: {final_tables}")
            
            print("\n" + "="*60)
            print("✅ PROCESO COMPLETADO")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    create_blog_tables()
