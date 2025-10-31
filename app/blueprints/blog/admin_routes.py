"""
Rutas de administración del blog (solo para admins)
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.blueprints.blog import blog_bp
from app.blueprints.blog.forms import BlogPostForm
from app.models.blog_post import BlogPost
from app.utils.markdown_utils import (
    generate_slug, 
    calculate_reading_time, 
    generate_excerpt,
    render_markdown
)
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
