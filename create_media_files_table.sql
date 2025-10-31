-- Crear tabla media_files en PostgreSQL
CREATE TABLE IF NOT EXISTS media_files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL UNIQUE,
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
    uploaded_by INTEGER NOT NULL,
    usage_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- Crear índices
CREATE INDEX IF NOT EXISTS ix_media_files_file_path ON media_files(file_path);
CREATE INDEX IF NOT EXISTS ix_media_files_uploaded_at ON media_files(uploaded_at);
