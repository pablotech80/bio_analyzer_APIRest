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
    """Eliminar post"""
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
    """Upload de archivos multimedia (imágenes, videos, audios)"""
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Guardar archivo
        file_info = save_uploaded_file(file)
        
        # Crear registro en base de datos
        media_file = MediaFile(
            filename=file_info['filename'],
            file_path=file_info['file_path'],
            file_url=file_info['file_url'],
            file_type=file_info['file_type'],
            mime_type=file_info['mime_type'],
            file_size=file_info['file_size'],
            width=file_info['width'],
            height=file_info['height'],
            duration=file_info['duration'],
            uploaded_by=current_user.id
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file': media_file.to_dict(),
            'markdown': media_file.markdown_embed
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al subir archivo: {str(e)}'}), 500


@blog_bp.route('/admin/media')
@admin_required
def admin_media():
    """Galería de medios"""
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
