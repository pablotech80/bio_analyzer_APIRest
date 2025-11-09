#!/usr/bin/env python3
"""
Script para probar el envío de emails desde terminal
Uso: python test_email.py
"""
import os
import sys
from flask import Flask
from app import create_app, db
from app.models.user import User
from app.services.email_service import send_notification_email, send_plans_ready_email
from app.models.notification import Notification

def test_email():
    """Probar envío de email"""
    print("=" * 60)
    print("🧪 TEST DE ENVÍO DE EMAILS - CoachBodyFit360")
    print("=" * 60)
    
    # Crear app
    app = create_app()
    
    with app.app_context():
        # Verificar configuración de email
        print("\n📧 Configuración de Email:")
        print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER', 'NO CONFIGURADO')}")
        print(f"   MAIL_PORT: {app.config.get('MAIL_PORT', 'NO CONFIGURADO')}")
        print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS', 'NO CONFIGURADO')}")
        print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME', 'NO CONFIGURADO')}")
        print(f"   MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER', 'NO CONFIGURADO')}")
        
        if not app.config.get('MAIL_SERVER'):
            print("\n❌ ERROR: No hay configuración de email en .env")
            print("\n📝 Agrega estas variables a tu archivo .env:")
            print("""
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
MAIL_DEFAULT_SENDER=tu_email@gmail.com
            """)
            return
        
        # Buscar un usuario de prueba
        print("\n👤 Buscando usuario de prueba...")
        user = User.query.first()
        
        if not user:
            print("❌ No hay usuarios en la base de datos")
            print("💡 Crea un usuario primero o usa la app web")
            return
        
        print(f"✅ Usuario encontrado: {user.first_name} {user.last_name} ({user.email})")
        
        # Menú de opciones
        print("\n" + "=" * 60)
        print("Selecciona el tipo de email a enviar:")
        print("=" * 60)
        print("1. Email de notificación genérica")
        print("2. Email de planes listos")
        print("3. Salir")
        print("=" * 60)
        
        opcion = input("\nOpción (1-3): ").strip()
        
        if opcion == "1":
            # Test de notificación
            print("\n📨 Enviando email de notificación...")
            
            # Crear notificación de prueba (sin guardar en BD)
            class FakeNotification:
                title = "🧪 Email de Prueba"
                message = "Este es un email de prueba desde el terminal. Si lo recibes, ¡todo funciona correctamente! 🎉"
                type = "info"
            
            notification = FakeNotification()
            
            resultado = send_notification_email(user, notification)
            
            if resultado:
                print(f"✅ Email enviado correctamente a {user.email}")
                print("📬 Revisa tu bandeja de entrada (puede tardar unos segundos)")
            else:
                print("❌ Error al enviar email (revisa los logs)")
        
        elif opcion == "2":
            # Test de planes listos
            print("\n📨 Enviando email de planes listos...")
            
            resultado = send_plans_ready_email(
                user=user,
                nutrition_plans_count=2,
                training_plans_count=1
            )
            
            if resultado:
                print(f"✅ Email enviado correctamente a {user.email}")
                print("📬 Revisa tu bandeja de entrada (puede tardar unos segundos)")
            else:
                print("❌ Error al enviar email (revisa los logs)")
        
        elif opcion == "3":
            print("\n👋 Saliendo...")
            return
        
        else:
            print("\n❌ Opción inválida")
            return
        
        print("\n" + "=" * 60)
        print("✅ Test completado")
        print("=" * 60)


if __name__ == "__main__":
    try:
        test_email()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
