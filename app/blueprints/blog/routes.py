"""
Rutas públicas del blog
"""

import logging

from flask import jsonify, render_template, request

from app import db
from app.blueprints.blog import blog_bp
from app.models.blog_post import BlogPost
from app.utils.markdown_utils import render_markdown
logger = logging.getLogger(__name__)


@blog_bp.route("/health")
def health():
    """Health check endpoint para debugging"""
    try:
        # Verificar que la tabla existe
        count = BlogPost.query.count()
        return jsonify({"status": "ok", "blog_posts_count": count, "database": "connected"}), 200
    except Exception as e:
        logger.error(f"Blog health check failed: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "error": str(e), "database": "error"}), 500


@blog_bp.route("/")
def index():
    """Listado de posts del blog"""
    try:
        # Paginación
        page = request.args.get("page", 1, type=int)
        per_page = 12

        # Filtro por categoría
        category = request.args.get("category")

        # Query base: solo posts publicados, ordenados por fecha
        query = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc())

        # Filtrar por categoría si se especifica
        if category:
            query = query.filter_by(category=category)

        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        posts = pagination.items

        # Posts destacados (3 más vistos)
        featured_posts = (
            BlogPost.query.filter_by(is_published=True)
            .order_by(BlogPost.views_count.desc())
            .limit(3)
            .all()
        )

        # Categorías con conteo
        categories = (
            db.session.query(BlogPost.category, db.func.count(BlogPost.id).label("count"))
            .filter_by(is_published=True)
            .group_by(BlogPost.category)
            .all()
        )

        return render_template(
            "blog/index.html",
            posts=posts,
            pagination=pagination,
            featured_posts=featured_posts,
            categories=categories,
            current_category=category,
        )
    except Exception as e:
        logger.error(f"Error in blog index: {str(e)}", exc_info=True)
        return render_template(
            "blog/index.html",
            posts=[],
            pagination=None,
            featured_posts=[],
            categories=[],
            current_category=None,
            error=str(e),
        )


@blog_bp.route("/<slug>")
def post(slug):
    """Ver un post individual"""
    # Buscar post por slug
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Incrementar contador de vistas
    post.views_count += 1
    db.session.commit()

    # Renderizar Markdown a HTML
    content_html = render_markdown(post.content)

    # Posts relacionados (misma categoría, excluyendo el actual)
    related_posts = (
        BlogPost.query.filter_by(category=post.category, is_published=True)
        .filter(BlogPost.id != post.id)
        .order_by(BlogPost.published_at.desc())
        .limit(3)
        .all()
    )

    return render_template(
        "blog/post.html", post=post, content_html=content_html, related_posts=related_posts
    )


@blog_bp.route("/categoria/<category>")
def category(category):
    """Posts filtrados por categoría"""
    # Redirigir a index con parámetro de categoría
    return index()


@blog_bp.route("/buscar")
def search():
    """Búsqueda de posts"""
    query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    per_page = 12

    if not query:
        return render_template("blog/search.html", posts=[], query="")

    # Buscar en título, excerpt y contenido
    search_filter = db.or_(
        BlogPost.title.ilike(f"%{query}%"),
        BlogPost.excerpt.ilike(f"%{query}%"),
        BlogPost.content.ilike(f"%{query}%"),
        BlogPost.tags.ilike(f"%{query}%"),
    )

    pagination = (
        BlogPost.query.filter(search_filter, BlogPost.is_published.is_(True))
        .order_by(BlogPost.published_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    posts = pagination.items

    return render_template("blog/search.html", posts=posts, pagination=pagination, query=query)
