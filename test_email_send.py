#!/usr/bin/env python3
"""
Script para probar envío de emails directamente
Uso: python test_email_send.py <email_destino>
"""
import sys
from app import create_app
from flask_mail import Message
from app import mail
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_email(recipient_email):
    """Probar envío de email"""
    print("="*70)
    print("📧 TEST: Envío de Email")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        # Verificar configuración
        print("\n1️⃣ Verificando configuración de email...")
        print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"   MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
        print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
        print(f"   MAIL_PASSWORD: {'***' if app.config.get('MAIL_PASSWORD') else 'NO CONFIGURADO'}")
        print(f"   MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
        
        if not app.config.get('MAIL_SERVER'):
            print("\n❌ MAIL_SERVER no configurado")
            return
        
        # Crear mensaje de prueba
        print(f"\n2️⃣ Creando mensaje de prueba para: {recipient_email}")
        
        msg = Message(
            subject="🧪 Test de Email - CoachBodyFit360",
            recipients=[recipient_email],
            sender=app.config.get('MAIL_DEFAULT_SENDER', 'noreply@coachbodyfit360.com')
        )
        
        msg.body = f"""
Hola,

Este es un email de prueba del sistema CoachBodyFit360.

Si recibes este mensaje, significa que el sistema de emails está funcionando correctamente.

---
CoachBodyFit360
        """
        
        msg.html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0;">🧪 Test de Email</h1>
    </div>
    
    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
        <p>Hola,</p>
        
        <p>Este es un email de prueba del sistema <strong>CoachBodyFit360</strong>.</p>
        
        <p>Si recibes este mensaje, significa que el sistema de emails está funcionando correctamente.</p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <p style="text-align: center; color: #999; font-size: 12px;">
            <strong>CoachBodyFit360</strong><br>
            Tu entrenador personal con IA
        </p>
    </div>
</body>
</html>
        """
        
        # Intentar enviar
        print(f"\n3️⃣ Intentando enviar email...")
        
        try:
            mail.send(msg)
            print(f"✅ Email enviado exitosamente a {recipient_email}")
            print(f"\n📬 Revisa tu bandeja de entrada:")
            print(f"   - Bandeja principal")
            print(f"   - Carpeta de spam/correo no deseado")
            print(f"   - Carpeta de promociones (Gmail)")
            print(f"\n⏰ Puede tardar 1-2 minutos en llegar")
            
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")
            print(f"\nDetalles del error:")
            import traceback
            traceback.print_exc()
            
            print(f"\n💡 Posibles causas:")
            print(f"   1. Contraseña de aplicación de Gmail incorrecta")
            print(f"   2. Verificación en 2 pasos no activada en Gmail")
            print(f"   3. Gmail bloqueando el acceso desde la app")
            print(f"   4. Firewall o antivirus bloqueando SMTP")
        
        print("\n" + "="*70)

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("📧 TEST: Envío de Email")
        print("="*70)
        print("\nUso: python test_email_send.py <email_destino>")
        print("\nEjemplos:")
        print("  python test_email_send.py ptecherasosa@icloud.com")
        print("  python test_email_send.py tu_email@gmail.com")
        print("="*70)
        return
    
    recipient = sys.argv[1]
    test_email(recipient)

if __name__ == "__main__":
    main()
