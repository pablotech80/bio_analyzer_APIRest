# app/blueprints/contact/routes.py
"""
Rutas para sistema de contacto
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app import db, csrf
from app.blueprints.contact import contact_bp
from app.blueprints.contact.forms import ContactForm
from app.models.biometric_analysis import BiometricAnalysis
from app.models.contact_message import ContactMessage


@contact_bp.route('/', methods=['GET', 'POST'])
@login_required
def send_message():
    """
    Mostrar formulario de contacto y procesar envío de mensaje
    """
    form = ContactForm()
    
    # Llenar opciones de análisis del usuario
    analyses = BiometricAnalysis.query.filter_by(user_id=current_user.id).order_by(BiometricAnalysis.created_at.desc()).all()
    form.analysis_id.choices = [(0, 'Ninguno (consulta general)')] + [(a.id, f'Análisis #{a.id} - {a.created_at.strftime("%d/%m/%Y")}') for a in analyses]
    
    if form.validate_on_submit():
        # Crear mensaje
        analysis_id = form.analysis_id.data if form.analysis_id.data != 0 else None
        
        message = ContactMessage(
            user_id=current_user.id,
            subject=form.subject.data,
            message=form.message.data,
            analysis_id=analysis_id
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('✅ Mensaje enviado correctamente. Te responderé lo antes posible.', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', form=form)


@contact_bp.route('/admin/mensajes')
@login_required
def admin_messages():
    """
    Panel de administrador: ver todos los mensajes
    Solo accesible para usuarios admin
    """
    if not current_user.is_admin:
        flash('⛔ Acceso denegado. Solo administradores.', 'danger')
        return redirect(url_for('index'))
    
    # Filtro opcional para ver solo no leídos
    show_unread = request.args.get('unread', type=int, default=0)
    
    query = ContactMessage.query
    
    if show_unread:
        query = query.filter_by(is_read=False)
    
    messages = query.order_by(ContactMessage.created_at.desc()).all()
    unread_count = ContactMessage.query.filter_by(is_read=False).count()
    total_count = ContactMessage.query.count()
    
    return render_template(
        'admin_messages.html',
        messages=messages,
        unread_count=unread_count,
        total_count=total_count,
        show_unread=bool(show_unread)
    )


@contact_bp.route('/admin/mensaje/<int:message_id>/leer')
@login_required
def mark_read(message_id):
    """
    Marcar mensaje como leído (solo admin)
    """
    if not current_user.is_admin:
        flash('⛔ Acceso denegado.', 'danger')
        return redirect(url_for('index'))
    
    message = ContactMessage.query.get_or_404(message_id)
    message.mark_as_read()
    
    flash(f'✅ Mensaje de {message.user.username} marcado como leído.', 'success')
    return redirect(url_for('contact.admin_messages'))
