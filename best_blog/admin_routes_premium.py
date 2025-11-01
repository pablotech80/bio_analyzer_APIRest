# app/blueprints/blog/admin_routes_premium.py
"""
Rutas del Dashboard Premium del Blog
Incluye integraciones con Nano Banana y NotebookLM
"""
from flask import render_template, request, jsonify, session, send_file
from flask_login import login_required, current_user
from app.blueprints.blog import blog_bp
from app import db
from app.models import BlogPost, MediaFile, User
from app.services.storage_service import StorageService
from app.services.nano_banana_service import NanoBananaService
from app.services.notebooklm_service import NotebookLMService
from app.services.seo_service import SEOService
from werkzeug.utils import secure_filename
import os
from datetime import datetime


# ============================================================================
# DASHBOARD PRINCIPAL
# ============================================================================

@blog_bp.route('/admin/dashboard-premium')
@login_required
def admin_dashboard_premium():
    """
    Dashboard premium de creación de posts
    
    Features:
    - Editor híbrido Markdown + Visual
    - Galería de medios integrada
    - Integración Nano Banana
    - Integración NotebookLM
    - SEO automático
    - Auto-save
    """
    if not current_user.is_admin:
        return "Acceso denegado", 403
    
    return render_template('blog/dashboard_premium.html')


@blog_bp.route('/admin/post/<int:post_id>/edit-premium')
@login_required
def admin_edit_premium(post_id):
    """Editar post existente en dashboard premium"""
    if not current_user.is_admin:
        return "Acceso denegado", 403
    
    post = BlogPost.query.get_or_404(post_id)
    
    return render_template(
        'blog/dashboard_premium.html',
        post=post,
        mode='edit'
    )


# ============================================================================
# API DE AUTO-SAVE
# ============================================================================

@blog_bp.route('/api/posts/autosave', methods=['POST'])
@login_required
def api_autosave():
    """
    Auto-guardado del post cada 30 segundos
    
    Body JSON:
    {
        "post_id": 123 (opcional, si es edición),
        "title": "...",
        "content": "...",
        "excerpt": "...",
        "slug": "...",
        "category": "...",
        "tags": ["tag1", "tag2"],
        "featured_image_id": 456,
        "scheduled_at": "2025-12-01T10:00:00"
    }
    
    Response:
    {
        "success": true,
        "post_id": 123,
        "saved_at": "2025-11-01T15:30:00",
        "seo_score": 85
    }
    """
    try:
        data = request.get_json()
        
        # Si hay post_id, actualizar; si no, crear borrador
        post_id = data.get('post_id')
        
        if post_id:
            post = BlogPost.query.get_or_404(post_id)
        else:
            post = BlogPost()
            post.author_id = current_user.id
            post.status = 'draft'
            db.session.add(post)
        
        # Actualizar campos
        post.title = data.get('title', '')
        post.content = data.get('content', '')
        post.excerpt = data.get('excerpt', '')
        post.slug = data.get('slug', '')
        post.category = data.get('category', '')
        
        # Tags (separados por coma)
        tags = data.get('tags', [])
        post.tags = ','.join(tags) if isinstance(tags, list) else tags
        
        # Imagen destacada
        if data.get('featured_image_id'):
            media = MediaFile.query.get(data['featured_image_id'])
            if media:
                post.featured_image = media.file_url
        
        # Fecha programada
        if data.get('scheduled_at'):
            post.scheduled_at = datetime.fromisoformat(data['scheduled_at'])
            post.status = 'scheduled'
        
        db.session.commit()
        
        # Calcular SEO score
        seo_score = SEOService.calculate_score(post)
        
        return jsonify({
            'success': True,
            'post_id': post.id,
            'saved_at': datetime.utcnow().isoformat(),
            'seo_score': seo_score
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API DE PUBLICACIÓN
# ============================================================================

@blog_bp.route('/api/posts/publish', methods=['POST'])
@login_required
def api_publish_post():
    """
    Publicar post inmediatamente
    
    Body JSON:
    {
        "post_id": 123
    }
    
    Response:
    {
        "success": true,
        "post_id": 123,
        "published_at": "...",
        "url": "/blog/mi-post"
    }
    """
    try:
        data = request.get_json()
        post_id = data.get('post_id')
        
        if not post_id:
            return jsonify({
                'success': False,
                'error': 'post_id requerido'
            }), 400
        
        post = BlogPost.query.get_or_404(post_id)
        
        # Validaciones
        if not post.title:
            return jsonify({
                'success': False,
                'error': 'El post necesita un título'
            }), 400
        
        if len(post.content or '') < 100:
            return jsonify({
                'success': False,
                'error': 'El contenido es demasiado corto (mínimo 100 caracteres)'
            }), 400
        
        # Publicar
        post.status = 'published'
        post.published_at = datetime.utcnow()
        
        # Generar meta description si no existe
        if not post.excerpt:
            post.excerpt = SEOService.generate_meta_description(post.content)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'post_id': post.id,
            'published_at': post.published_at.isoformat(),
            'url': f'/blog/{post.slug}',
            'message': '🎉 ¡Post publicado exitosamente!'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API DE MEDIOS
# ============================================================================

@blog_bp.route('/api/media/list', methods=['GET'])
@login_required
def api_media_list():
    """
    Listar archivos multimedia
    
    Query params:
    - type: image, video, audio (opcional)
    - page: número de página (default: 1)
    - per_page: items por página (default: 24)
    - search: término de búsqueda
    
    Response:
    {
        "items": [...],
        "total": 150,
        "page": 1,
        "per_page": 24,
        "pages": 7
    }
    """
    try:
        file_type = request.args.get('type')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 24, type=int)
        search = request.args.get('search', '')
        
        # Query base
        query = MediaFile.query
        
        # Filtrar por tipo
        if file_type:
            query = query.filter_by(file_type=file_type)
        
        # Buscar
        if search:
            query = query.filter(
                db.or_(
                    MediaFile.filename.ilike(f'%{search}%'),
                    MediaFile.title.ilike(f'%{search}%')
                )
            )
        
        # Ordenar por reciente
        query = query.order_by(MediaFile.uploaded_at.desc())
        
        # Paginar
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        items = [media.to_dict() for media in pagination.items]
        
        return jsonify({
            'items': items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@blog_bp.route('/api/media/upload', methods=['POST'])
@login_required
def api_media_upload():
    """
    Upload de archivos multimedia
    
    Soporta:
    - Imágenes: JPG, PNG, WEBP, GIF
    - Videos: MP4, WEBM
    - Audios: MP3, WAV, OGG (NotebookLM)
    
    Form data:
    - file: archivo (requerido)
    - title: título (opcional)
    - alt_text: texto alternativo (opcional)
    
    Response:
    {
        "success": true,
        "file": {
            "id": 123,
            "url": "https://cdn.../image.webp",
            "thumbnail_url": "https://cdn.../image_thumb.webp",
            ...
        }
    }
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se envió ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Archivo sin nombre'
            }), 400
        
        # Guardar archivo (usa S3 si está configurado)
        storage = StorageService()
        file_info = storage.save_file(file)
        
        # Crear registro en BD
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
        
        return jsonify({
            'success': True,
            'file': media_file.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# INTEGRACIÓN NANO BANANA
# ============================================================================

@blog_bp.route('/api/nano-banana/generate', methods=['POST'])
@login_required
def api_nano_banana_generate():
    """
    Generar imagen con Nano Banana
    
    Body JSON:
    {
        "prompt": "A muscular athlete lifting weights in a gym",
        "style": "realistic", (opcional)
        "size": "1024x1024" (opcional)
    }
    
    Response:
    {
        "success": true,
        "image_url": "https://...",
        "media_id": 123
    }
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt requerido'
            }), 400
        
        # Generar imagen con Nano Banana
        nb_service = NanoBananaService()
        image_url = nb_service.generate_image(
            prompt=prompt,
            style=data.get('style', 'realistic'),
            size=data.get('size', '1024x1024')
        )
        
        # Descargar y guardar en S3
        storage = StorageService()
        file_info = storage.save_from_url(image_url)
        
        # Crear registro
        media_file = MediaFile(
            filename=file_info['filename'],
            file_path=file_info['file_path'],
            file_url=file_info['file_url'],
            file_type='image',
            mime_type='image/png',
            file_size=file_info['file_size'],
            width=file_info.get('width'),
            height=file_info.get('height'),
            title=f"Generado con IA: {prompt[:50]}",
            alt_text=prompt,
            caption=f"Imagen generada con Nano Banana",
            uploaded_by=current_user.id
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'image_url': media_file.file_url,
            'media_id': media_file.id,
            'message': '✨ Imagen generada con éxito'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# INTEGRACIÓN NOTEBOOKLM
# ============================================================================

@blog_bp.route('/api/notebooklm/upload-audio', methods=['POST'])
@login_required
def api_notebooklm_upload():
    """
    Upload de audio de NotebookLM
    
    Form data:
    - file: archivo de audio (requerido)
    - title: título del podcast (opcional)
    - transcript: transcripción (opcional)
    
    Response:
    {
        "success": true,
        "audio": {
            "id": 123,
            "url": "https://cdn.../podcast.mp3",
            "duration": 180,
            "embed_code": "<audio>...</audio>"
        }
    }
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se envió archivo de audio'
            }), 400
        
        file = request.files['file']
        
        # Validar que es audio
        if not file.mimetype.startswith('audio/'):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser de audio'
            }), 400
        
        # Guardar archivo
        storage = StorageService()
        file_info = storage.save_file(file)
        
        # Crear registro
        media_file = MediaFile(
            filename=file_info['filename'],
            file_path=file_info['file_path'],
            file_url=file_info['file_url'],
            file_type='audio',
            mime_type=file_info['mime_type'],
            file_size=file_info['file_size'],
            duration=file_info.get('duration'),
            title=request.form.get('title', 'Podcast NotebookLM'),
            caption=request.form.get('transcript', ''),
            uploaded_by=current_user.id
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        # Generar código de embed
        embed_code = f'''
        <audio controls style="width: 100%;">
            <source src="{media_file.file_url}" type="{media_file.mime_type}">
            Tu navegador no soporta audio HTML5.
        </audio>
        '''
        
        return jsonify({
            'success': True,
            'audio': {
                'id': media_file.id,
                'url': media_file.file_url,
                'duration': media_file.duration,
                'embed_code': embed_code.strip()
            },
            'message': '🎙️ Audio subido exitosamente'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API DE SEO
# ============================================================================

@blog_bp.route('/api/seo/analyze', methods=['POST'])
@login_required
def api_seo_analyze():
    """
    Analizar SEO del post
    
    Body JSON:
    {
        "title": "...",
        "content": "...",
        "excerpt": "..."
    }
    
    Response:
    {
        "score": 85,
        "issues": [],
        "suggestions": [],
        "keywords": ["fitness", "entrenamiento", ...]
    }
    """
    try:
        data = request.get_json()
        
        analysis = SEOService.analyze_post(
            title=data.get('title', ''),
            content=data.get('content', ''),
            excerpt=data.get('excerpt', '')
        )
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API DE IA - MEJORA DE CONTENIDO
# ============================================================================

@blog_bp.route('/api/ai/improve-content', methods=['POST'])
@login_required
def api_ai_improve():
    """
    Mejorar contenido con IA (OpenAI GPT-4)
    
    Body JSON:
    {
        "content": "...",
        "action": "improve" | "shorten" | "expand" | "simplify"
    }
    
    Response:
    {
        "success": true,
        "improved_content": "..."
    }
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        action = data.get('action', 'improve')
        
        # Implementar con OpenAI API
        # improved = OpenAIService.improve_content(content, action)
        
        # Por ahora, placeholder
        improved = f"[Contenido mejorado con IA - {action}]\n\n{content}"
        
        return jsonify({
            'success': True,
            'improved_content': improved
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API DE BLOQUES REUTILIZABLES
# ============================================================================

@blog_bp.route('/api/blocks/list', methods=['GET'])
@login_required
def api_blocks_list():
    """
    Listar bloques reutilizables
    
    Response:
    {
        "blocks": [
            {
                "id": 1,
                "name": "CTA Newsletter",
                "type": "cta",
                "content": "...",
                "preview": "..."
            },
            ...
        ]
    }
    """
    # Implementar con modelo ContentBlock
    blocks = [
        {
            'id': 1,
            'name': 'CTA Newsletter',
            'type': 'cta',
            'content': '<div class="cta">Suscríbete al newsletter</div>',
            'preview': 'https://...'
        },
        # Más bloques...
    ]
    
    return jsonify({'blocks': blocks}), 200
