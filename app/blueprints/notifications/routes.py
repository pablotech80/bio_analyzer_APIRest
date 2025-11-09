"""
Blueprint de notificaciones para usuarios
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.notification import Notification

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notificaciones")


@notifications_bp.route("/")
@login_required
def index():
    """Ver todas las notificaciones del usuario"""
    # Obtener todas las notificaciones del usuario ordenadas por fecha
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()
    
    # Contar no leídas
    unread_count = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
    
    return render_template(
        "notifications/index.html",
        notifications=notifications,
        unread_count=unread_count
    )


@notifications_bp.route("/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_as_read(notification_id):
    """Marcar notificación como leída"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Verificar que la notificación pertenece al usuario
    if notification.user_id != current_user.id:
        flash("❌ No tienes permiso para acceder a esta notificación", "danger")
        return redirect(url_for("notifications.index"))
    
    notification.mark_as_read()
    return redirect(url_for("notifications.index"))


@notifications_bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    """Marcar todas las notificaciones como leídas"""
    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update({"is_read": True})
    
    db.session.commit()
    flash("✅ Todas las notificaciones marcadas como leídas", "success")
    return redirect(url_for("notifications.index"))


@notifications_bp.route("/<int:notification_id>/delete", methods=["POST"])
@login_required
def delete(notification_id):
    """Eliminar notificación"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Verificar que la notificación pertenece al usuario
    if notification.user_id != current_user.id:
        flash("❌ No tienes permiso para eliminar esta notificación", "danger")
        return redirect(url_for("notifications.index"))
    
    db.session.delete(notification)
    db.session.commit()
    flash("✅ Notificación eliminada", "success")
    return redirect(url_for("notifications.index"))
