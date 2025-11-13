#!/usr/bin/env python3
"""
Script para probar el sistema de recuperación de contraseñas
Uso: python test_password_reset.py <email>
"""
import sys
from app import create_app
from app.blueprints.auth.services import AuthService
from app.services.email_service import send_password_reset_email
from flask import url_for

def test_password_reset(email):
    """Probar el sistema de reset de contraseña"""
    print("="*70)
    print("🧪 TEST: Sistema de Recuperación de Contraseñas")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        print(f"\n1️⃣ Generando token para: {email}")
        
        # Generar token
        user, token = AuthService.generate_password_reset_token(email)
        
        if not user:
            print(f"❌ Usuario no encontrado: {email}")
            return
        
        print(f"✅ Token generado para: {user.first_name} {user.last_name}")
        print(f"   Token: {token[:20]}...")
        print(f"   Expira en: 1 hora")
        
        # Generar URL de reset
        with app.test_request_context():
            reset_url = url_for("auth.reset_password", token=token, _external=True)
        
        print(f"\n2️⃣ URL de reset generada:")
        print(f"   {reset_url}")
        
        # Intentar enviar email
        print(f"\n3️⃣ Enviando email a: {user.email}")
        
        email_sent = send_password_reset_email(user, reset_url)
        
        if email_sent:
            print(f"✅ Email enviado exitosamente!")
            print(f"\n📧 Revisa la bandeja de entrada de: {user.email}")
            print(f"   (También revisa la carpeta de spam)")
        else:
            print(f"❌ Error al enviar email")
            print(f"\n💡 Puedes usar este link manualmente:")
            print(f"   {reset_url}")
        
        print("\n" + "="*70)
        print("✅ TEST COMPLETADO")
        print("="*70)

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("🧪 TEST: Sistema de Recuperación de Contraseñas")
        print("="*70)
        print("\nUso: python test_password_reset.py <email>")
        print("\nEjemplos:")
        print("  python test_password_reset.py xxzeus16@hotmail.com")
        print("  python test_password_reset.py ptecherasosa@icloud.com")
        print("="*70)
        return
    
    email = sys.argv[1]
    test_password_reset(email)

if __name__ == "__main__":
    main()
