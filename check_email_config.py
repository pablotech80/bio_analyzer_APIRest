#!/usr/bin/env python3
"""
Script para verificar configuración de email
Uso: python check_email_config.py
"""
from app import create_app

def check_config():
    """Verificar configuración de email"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        config_items = [
            ('MAIL_SERVER', app.config.get('MAIL_SERVER')),
            ('MAIL_PORT', app.config.get('MAIL_PORT')),
            ('MAIL_USE_TLS', app.config.get('MAIL_USE_TLS')),
            ('MAIL_USERNAME', app.config.get('MAIL_USERNAME')),
            ('MAIL_PASSWORD', '***' if app.config.get('MAIL_PASSWORD') else None),
            ('MAIL_DEFAULT_SENDER', app.config.get('MAIL_DEFAULT_SENDER')),
        ]
        
        print("\n📧 Configuración actual:")
        all_configured = True
        for key, value in config_items:
            status = "✅" if value else "❌"
            print(f"   {status} {key}: {value if value else 'NO CONFIGURADO'}")
            if not value:
                all_configured = False
        
        print("\n" + "=" * 60)
        if all_configured:
            print("✅ CONFIGURACIÓN COMPLETA - Los emails deberían funcionar")
        else:
            print("❌ CONFIGURACIÓN INCOMPLETA - Faltan variables de entorno")
            print("\n📝 Agrega estas variables a tu .env (desarrollo) o Railway (producción):")
            print("""
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
MAIL_DEFAULT_SENDER=tu_email@gmail.com
            """)
        print("=" * 60)

if __name__ == "__main__":
    check_config()
