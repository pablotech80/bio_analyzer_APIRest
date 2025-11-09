"""
Servicio de envío de emails
"""
from flask import render_template, current_app
from flask_mail import Message
from app import mail
import logging
from threading import Thread

logger = logging.getLogger(__name__)


def send_async_email(app, msg):
    """Enviar email en thread separado"""
    with app.app_context():
        try:
            logger.info(f"Intentando enviar email a {msg.recipients}")
            mail.send(msg)
            logger.info(f"✅ Email enviado exitosamente a {msg.recipients}")
        except Exception as e:
            logger.error(f"❌ Error al enviar email async a {msg.recipients}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())


def send_notification_email(user, notification):
    """
    Enviar email de notificación al usuario
    
    Args:
        user: Usuario destinatario
        notification: Objeto Notification
    
    Returns:
        bool: True si se envió correctamente, False si falló
    """
    try:
        # Verificar que el email esté configurado
        if not current_app.config.get('MAIL_SERVER'):
            logger.warning("MAIL_SERVER no configurado. Email no enviado.")
            return False
        
        # Crear mensaje
        msg = Message(
            subject=notification.title,
            recipients=[user.email],
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@coachbodyfit360.com')
        )
        
        # Cuerpo en texto plano
        msg.body = notification.message
        
        # Cuerpo en HTML (más bonito)
        msg.html = render_template(
            'emails/notification.html',
            user=user,
            notification=notification
        )
        
        # Enviar en thread separado (no bloquea la respuesta)
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        logger.info(f"Email programado para envío a {user.email}: {notification.title}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar email a {user.email}: {str(e)}")
        return False


def send_plans_ready_email(user, nutrition_plans_count, training_plans_count):
    """
    Enviar email cuando los planes están listos
    
    Args:
        user: Usuario destinatario
        nutrition_plans_count: Cantidad de planes de nutrición
        training_plans_count: Cantidad de planes de entrenamiento
    
    Returns:
        bool: True si se envió correctamente
    """
    try:
        logger.info(f"📧 Iniciando envío de email de planes listos a {user.email}")
        
        # Verificar que el email esté configurado
        if not current_app.config.get('MAIL_SERVER'):
            logger.warning("❌ MAIL_SERVER no configurado. Email no enviado.")
            return False
        
        logger.info(f"✅ MAIL_SERVER configurado: {current_app.config.get('MAIL_SERVER')}")
        
        # Crear mensaje
        msg = Message(
            subject="🎉 ¡Tus planes están listos!",
            recipients=[user.email],
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@coachbodyfit360.com')
        )

        # Texto plano
        msg.body = f"""
Hola {user.first_name},

¡Buenas noticias! Tu entrenador ha preparado tus planes personalizados:

✅ {nutrition_plans_count} plan(es) de nutrición
✅ {training_plans_count} plan(es) de entrenamiento

Puedes verlos en tu dashboard: https://app.coachbodyfit360.com

¡A por ello! 💪

---
CoachBodyFit360
Tu entrenador personal con IA
        """

        # HTML
        msg.html = render_template(
            'emails/plans_ready.html',
            user=user,
            nutrition_plans_count=nutrition_plans_count,
            training_plans_count=training_plans_count
        )

        # Enviar en thread separado (no bloquea la respuesta)
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        logger.info(f"Email de planes listos programado para {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar email a {user.email}: {str(e)}")
        return False
