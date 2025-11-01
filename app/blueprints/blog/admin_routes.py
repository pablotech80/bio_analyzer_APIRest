"""
Rutas de administración del blog (solo para admins)
"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.blog import blog_bp
from app.blueprints.blog.forms import BlogPostForm
from app.models.blog_post import BlogPost
from app.models.media_file import MediaFile
from app.utils.markdown_utils import (
    generate_slug, 
    calculate_reading_time, 
    generate_excerpt,
    render_markdown
)
from app.utils.file_upload import save_uploaded_file, delete_file
from app.services.storage_service import get_storage_service
from app import db
from datetime import datetime
from functools import wraps


def admin_required(f):
    """Decorador para requerir permisos de admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('blog.index'))
        return f(*args, **kwargs)
    return decorated_function


@blog_bp.route('/admin')
@admin_required
def admin_dashboard():
    """Dashboard de administración del blog"""
    try:
        # Estadísticas
        total_posts = BlogPost.query.count()
        published_posts = BlogPost.query.filter_by(is_published=True).count()
        draft_posts = BlogPost.query.filter_by(is_published=False).count()
        total_views = db.session.query(db.func.sum(BlogPost.views_count)).scalar() or 0
        
        # Todos los posts (publicados y drafts)
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        
        return render_template(
            'blog/admin_dashboard.html',
            posts=posts,
            total_posts=total_posts,
            published_posts=published_posts,
            draft_posts=draft_posts,
            total_views=total_views
        )
    except Exception as e:
        flash(f'Error al cargar el dashboard del blog: {str(e)}', 'danger')
        return render_template(
            'blog/admin_dashboard.html',
            posts=[],
            total_posts=0,
            published_posts=0,
            draft_posts=0,
            total_views=0,
            error=str(e)
        )


@blog_bp.route('/admin/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_new():
    """Crear nuevo post"""
    form = BlogPostForm()
    
    if form.validate_on_submit():
        # Generar slug desde el título
        slug = generate_slug(form.title.data)
        
        # Verificar que el slug sea único
        existing_post = BlogPost.query.filter_by(slug=slug).first()
        if existing_post:
            slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Calcular tiempo de lectura
        reading_time = calculate_reading_time(form.content.data)
        
        # Generar excerpt si no se proporcionó
        excerpt = form.excerpt.data or generate_excerpt(form.content.data)
        
        # Crear post
        post = BlogPost(
            title=form.title.data,
            slug=slug,
            excerpt=excerpt,
            content=form.content.data,
            featured_image=form.featured_image.data,
            category=form.category.data,
            tags=form.tags.data,
            meta_description=form.meta_description.data or excerpt,
            meta_keywords=form.meta_keywords.data,
            author_id=current_user.id,
            is_published=form.is_published.data,
            published_at=datetime.utcnow() if form.is_published.data else None,
            reading_time=reading_time
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash(f'Post "{post.title}" creado exitosamente!', 'success')
        return redirect(url_for('blog.admin_dashboard'))
    
    return render_template('blog/admin_editor.html', form=form, post=None)


@blog_bp.route('/admin/editar/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(post_id):
    """Editar post existente"""
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)
    
    if form.validate_on_submit():
        # Actualizar slug si cambió el título
        if form.title.data != post.title:
            new_slug = generate_slug(form.title.data)
            existing_post = BlogPost.query.filter_by(slug=new_slug).filter(BlogPost.id != post.id).first()
            if not existing_post:
                post.slug = new_slug
        
        # Actualizar campos
        post.title = form.title.data
        post.excerpt = form.excerpt.data or generate_excerpt(form.content.data)
        post.content = form.content.data
        post.featured_image = form.featured_image.data
        post.category = form.category.data
        post.tags = form.tags.data
        post.meta_description = form.meta_description.data or post.excerpt
        post.meta_keywords = form.meta_keywords.data
        post.reading_time = calculate_reading_time(form.content.data)
        
        # Si se publica por primera vez, establecer fecha
        if form.is_published.data and not post.is_published:
            post.published_at = datetime.utcnow()
        
        post.is_published = form.is_published.data
        
        db.session.commit()
        
        flash(f'Post "{post.title}" actualizado exitosamente!', 'success')
        return redirect(url_for('blog.admin_dashboard'))
    
    return render_template('blog/admin_editor.html', form=form, post=post)


@blog_bp.route('/admin/eliminar/<int:post_id>', methods=['POST'])
@admin_required
def admin_delete(post_id):
    """Eliminar post (requiere CSRF token)"""
    post = BlogPost.query.get_or_404(post_id)
    title = post.title
    
    db.session.delete(post)
    db.session.commit()
    
    flash(f'Post "{title}" eliminado exitosamente.', 'success')
    return redirect(url_for('blog.admin_dashboard'))


@blog_bp.route('/admin/preview/<int:post_id>')
@admin_required
def admin_preview(post_id):
    """Preview de post (incluso si no está publicado)"""
    post = BlogPost.query.get_or_404(post_id)
    content_html = render_markdown(post.content)
    
    return render_template(
        'blog/post.html',
        post=post,
        content_html=content_html,
        related_posts=[],
        is_preview=True
    )


@blog_bp.route('/admin/upload', methods=['POST'])
@admin_required
def admin_upload():
    """
    Upload de archivos multimedia CORREGIDO
    
    Maneja correctamente FileStorage con PIL y S3
    
    Form data:
    - file: archivo (imagen, video o audio)
    - title: título opcional
    - alt_text: texto alternativo opcional
    
    Response:
    {
        "success": true,
        "file": {
            "id": 123,
            "url": "https://...",
            "filename": "image.webp",
            ...
        },
        "markdown": "![alt text](url)"
    }
    """
    print("\n" + "="*50)
    print("=== INICIO UPLOAD ===")
    print("="*50)
    
    try:
        # 1. VERIFICAR QUE SE ENVIÓ UN ARCHIVO
        print(f"Files en request: {request.files}")
        
        if 'file' not in request.files:
            print("❌ No hay 'file' en request.files")
            return jsonify({
                'success': False,
                'error': 'No se envió ningún archivo'
            }), 400
        
        file = request.files['file']
        print(f"Archivo recibido: {file.filename}")
        print(f"Content-Type: {file.content_type}")
        
        if file.filename == '':
            print("❌ Filename está vacío")
            return jsonify({
                'success': False,
                'error': 'Archivo sin nombre'
            }), 400
        
        # 2. OBTENER SERVICIO DE ALMACENAMIENTO
        from flask import current_app
        storage = get_storage_service(current_app)
        
        if storage is None:
            print("❌ StorageService no inicializado")
            return jsonify({
                'success': False,
                'error': 'Servicio de almacenamiento no disponible'
            }), 500
        
        print(f"S3 configurado: {storage.use_s3}")
        
        # 3. GUARDAR ARCHIVO (aquí se hace toda la magia)
        # El StorageService maneja correctamente PIL y S3
        file_info = storage.save_file(file)
        
        print(f"✅ Archivo guardado exitosamente")
        print(f"   URL: {file_info['file_url']}")
        print(f"   Storage: {file_info.get('storage', 'unknown')}")
        
        # 4. CREAR REGISTRO EN BASE DE DATOS
        media_file = MediaFile(
            filename=file_info['filename'],
            file_path=file_info['file_path'],
            file_url=file_info['file_url'],
            file_type=file_info['file_type'],
            mime_type=file_info['mime_type'],
            file_size=file_info['file_size'],
            width=file_info.get('width'),
            height=file_info.get('height'),
            duration=file_info.get('duration'),
            title=request.form.get('title'),
            alt_text=request.form.get('alt_text'),
            uploaded_by=current_user.id
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        print(f"✅ MediaFile creado en BD con ID: {media_file.id}")
        
        # 5. RESPUESTA
        response_data = {
            'success': True,
            'file': media_file.to_dict(),
            'markdown': media_file.markdown_embed
        }
        
        print("="*50)
        print("=== UPLOAD EXITOSO ===")
        print("="*50 + "\n")
        
        return jsonify(response_data), 200
    
    except ValueError as e:
        # Error de validación (tipo de archivo no soportado, etc.)
        print(f"❌ ValueError en upload: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        # Error inesperado
        print(f"❌ Exception en upload: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Error al subir archivo: {str(e)}'
        }), 500


@blog_bp.route('/admin/media')
@admin_required
def admin_media():
    """Galería de medios"""
    try:
        # Filtros
        file_type = request.args.get('type')  # image, video, audio
        page = request.args.get('page', 1, type=int)
        per_page = 24
        
        # Query base
        query = MediaFile.query.order_by(MediaFile.uploaded_at.desc())
        
        # Filtrar por tipo si se especifica
        if file_type:
            query = query.filter_by(file_type=file_type)
        
        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        media_files = pagination.items
        
        # Estadísticas
        total_files = MediaFile.query.count()
        total_images = MediaFile.query.filter_by(file_type='image').count()
        total_videos = MediaFile.query.filter_by(file_type='video').count()
        total_audios = MediaFile.query.filter_by(file_type='audio').count()
        
        return render_template(
            'blog/admin_media.html',
            media_files=media_files,
            pagination=pagination,
            total_files=total_files,
            total_images=total_images,
            total_videos=total_videos,
            total_audios=total_audios,
            current_type=file_type
        )
    except Exception as e:
        flash(f'Error al cargar la galería de medios: {str(e)}', 'danger')
        return render_template(
            'blog/admin_media.html',
            media_files=[],
            pagination=None,
            total_files=0,
            total_images=0,
            total_videos=0,
            total_audios=0,
            current_type=file_type,
            error=str(e)
        )


@blog_bp.route('/admin/media/<int:media_id>/delete', methods=['POST'])
@admin_required
def admin_media_delete(media_id):
    """Eliminar archivo multimedia"""
    media_file = MediaFile.query.get_or_404(media_id)
    
    # Eliminar archivo físico
    delete_file(media_file.file_path)
    
    # Eliminar registro de BD
    db.session.delete(media_file)
    db.session.commit()
    
    flash(f'Archivo "{media_file.filename}" eliminado exitosamente.', 'success')
    return redirect(url_for('blog.admin_media'))


# ============================================================================
# RUTA ADICIONAL: Test de upload
# ============================================================================

@blog_bp.route('/admin/test-upload')
@admin_required
def admin_test_upload():
    """Página de prueba para verificar el upload"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Upload - CoachBodyFit360</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
            }
            .card {
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
                margin-bottom: 20px;
            }
            .card-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .card-header h1 {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .card-header p {
                opacity: 0.9;
                font-size: 16px;
            }
            .card-body {
                padding: 40px;
            }
            .upload-zone {
                border: 3px dashed #cbd5e0;
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                background: #f7fafc;
                transition: all 0.3s;
                cursor: pointer;
            }
            .upload-zone:hover {
                border-color: #667eea;
                background: #edf2f7;
            }
            .upload-zone.dragover {
                border-color: #667eea;
                background: #e6fffa;
            }
            .upload-icon {
                font-size: 48px;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                font-weight: 600;
                margin-bottom: 8px;
                color: #2d3748;
            }
            .form-control {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .form-control:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 32px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                width: 100%;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 12px;
                animation: slideIn 0.3s;
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .success {
                background: #d1fae5;
                border-left: 4px solid #10b981;
                color: #065f46;
            }
            .error {
                background: #fee2e2;
                border-left: 4px solid #ef4444;
                color: #991b1b;
            }
            .loading {
                background: #dbeafe;
                border-left: 4px solid #3b82f6;
                color: #1e40af;
            }
            .result h3 {
                margin-bottom: 15px;
                font-size: 20px;
            }
            .result-item {
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }
            .result-item:last-child {
                border-bottom: none;
            }
            .result-item strong {
                display: inline-block;
                min-width: 120px;
            }
            .result-item a {
                color: #667eea;
                text-decoration: none;
                word-break: break-all;
            }
            .result-item a:hover {
                text-decoration: underline;
            }
            .preview-image {
                max-width: 100%;
                margin-top: 20px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            code {
                background: #2d3748;
                color: #68d391;
                padding: 12px;
                border-radius: 8px;
                display: block;
                margin-top: 10px;
                font-family: 'Courier New', monospace;
                overflow-x: auto;
            }
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h1>🚀 Test de Upload S3</h1>
                    <p>Prueba el sistema de almacenamiento de archivos multimedia</p>
                </div>
                
                <div class="card-body">
                    <form id="uploadForm">
                        <div class="upload-zone" id="uploadZone">
                            <div class="upload-icon">📁</div>
                            <h3>Arrastra un archivo aquí</h3>
                            <p style="margin: 10px 0; color: #718096;">o haz click para seleccionar</p>
                            <input type="file" id="fileInput" accept="image/*,video/*,audio/*" style="display: none;">
                            <p style="font-size: 14px; color: #a0aec0; margin-top: 10px;">
                                Soportado: Imágenes, Videos, Audios
                            </p>
                        </div>
                        
                        <div class="form-group" style="margin-top: 30px;">
                            <label for="titleInput">📝 Título (opcional)</label>
                            <input type="text" id="titleInput" class="form-control" placeholder="Ej: Logo de CoachBodyFit360">
                        </div>
                        
                        <div class="form-group">
                            <label for="altTextInput">🏷️ Texto Alternativo (opcional)</label>
                            <input type="text" id="altTextInput" class="form-control" placeholder="Descripción para accesibilidad">
                        </div>
                        
                        <button type="submit" class="btn" id="submitBtn">
                            ⬆️ Subir Archivo
                        </button>
                    </form>
                    
                    <div id="result" style="display: none;"></div>
                </div>
            </div>
        </div>
        
        <script>
            const uploadZone = document.getElementById('uploadZone');
            const fileInput = document.getElementById('fileInput');
            const uploadForm = document.getElementById('uploadForm');
            const resultDiv = document.getElementById('result');
            const submitBtn = document.getElementById('submitBtn');
            
            // Click en zona de upload
            uploadZone.addEventListener('click', () => fileInput.click());
            
            // Drag & Drop
            uploadZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadZone.classList.add('dragover');
            });
            
            uploadZone.addEventListener('dragleave', () => {
                uploadZone.classList.remove('dragover');
            });
            
            uploadZone.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadZone.classList.remove('dragover');
                if (e.dataTransfer.files.length) {
                    fileInput.files = e.dataTransfer.files;
                    updateFileName();
                }
            });
            
            // Actualizar nombre de archivo
            fileInput.addEventListener('change', updateFileName);
            
            function updateFileName() {
                if (fileInput.files[0]) {
                    const fileName = fileInput.files[0].name;
                    const fileSize = (fileInput.files[0].size / 1024 / 1024).toFixed(2);
                    uploadZone.innerHTML = `
                        <div class="upload-icon">✅</div>
                        <h3>${fileName}</h3>
                        <p style="color: #718096; margin-top: 10px;">${fileSize} MB</p>
                        <p style="font-size: 14px; color: #a0aec0; margin-top: 10px;">
                            Click para cambiar archivo
                        </p>
                    `;
                }
            }
            
            // Submit form
            uploadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                if (!fileInput.files[0]) {
                    alert('❌ Selecciona un archivo primero');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('csrf_token', '{{ csrf_token() }}');
                
                const title = document.getElementById('titleInput').value;
                const altText = document.getElementById('altTextInput').value;
                
                if (title) formData.append('title', title);
                if (altText) formData.append('alt_text', altText);
                
                // Mostrar loading
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = `
                    <div class="spinner"></div>
                    <h3 style="text-align: center;">Subiendo archivo...</h3>
                `;
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/blog/admin/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `
                            <h3>✅ ¡Archivo subido exitosamente!</h3>
                            <div class="result-item"><strong>ID:</strong> ${data.file.id}</div>
                            <div class="result-item"><strong>Nombre:</strong> ${data.file.filename}</div>
                            <div class="result-item">
                                <strong>URL:</strong> 
                                <a href="${data.file.file_url}" target="_blank">${data.file.file_url}</a>
                            </div>
                            <div class="result-item"><strong>Tipo:</strong> ${data.file.file_type}</div>
                            <div class="result-item"><strong>Tamaño:</strong> ${data.file.file_size_human || 'N/A'}</div>
                            ${data.file.width ? `<div class="result-item"><strong>Dimensiones:</strong> ${data.file.width}x${data.file.height}px</div>` : ''}
                            <div class="result-item">
                                <strong>Markdown:</strong>
                                <code>${data.markdown}</code>
                            </div>
                            ${data.file.file_type === 'image' ? `
                                <img src="${data.file.file_url}" alt="${data.file.alt_text || data.file.filename}" class="preview-image">
                            ` : ''}
                        `;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `
                            <h3>❌ Error al subir archivo</h3>
                            <p>${data.error}</p>
                        `;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <h3>❌ Error de conexión</h3>
                        <p>${error.message}</p>
                    `;
                } finally {
                    submitBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    '''
    return html
