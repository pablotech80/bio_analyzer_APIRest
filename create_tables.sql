-- Crear tabla media_files
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

-- Crear tabla blog_posts
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
