#!/usr/bin/env python3
"""
Script para probar recuperación de contraseña en Railway
Uso: python test_password_reset_railway.py <email>
"""
import sys
from sqlalchemy import create_engine, text
from secrets import token_urlsafe
from datetime import datetime, timedelta

RAILWAY_DB_URL = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"

def test_password_reset(email):
    """Probar el sistema de reset de contraseña"""
    print("="*70)
    print("🧪 TEST: Sistema de Recuperación de Contraseñas (Railway)")
    print("="*70)
    
    try:
        engine = create_engine(RAILWAY_DB_URL, echo=False)
        
        with engine.connect() as conn:
            # Buscar usuario
            print(f"\n1️⃣ Buscando usuario: {email}")
            result = conn.execute(
                text("SELECT id, email, first_name, last_name FROM users WHERE email = :email"),
                {"email": email.lower()}
            )
            user = result.fetchone()
            
            if not user:
                print(f"❌ Usuario no encontrado: {email}")
                return
            
            print(f"✅ Usuario encontrado:")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Nombre: {user[2]} {user[3]}")
            
            # Generar token
            print(f"\n2️⃣ Generando token de reset...")
            token = token_urlsafe(32)
            expires = datetime.utcnow() + timedelta(hours=1)
            
            # Actualizar usuario con token
            conn.execute(
                text("""
                    UPDATE users 
                    SET reset_password_token = :token, 
                        reset_password_expires = :expires 
                    WHERE email = :email
                """),
                {"token": token, "expires": expires, "email": email.lower()}
            )
            conn.commit()
            
            print(f"✅ Token generado:")
            print(f"   Token: {token[:20]}...")
            print(f"   Expira: {expires}")
            
            # Generar URL
            reset_url = f"https://app.coachbodyfit360.com/auth/reset-password/{token}"
            
            print(f"\n3️⃣ URL de reset:")
            print(f"   {reset_url}")
            
            print(f"\n4️⃣ Simulación de email:")
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                  📧 EMAIL DE RECUPERACIÓN                        ║
╚══════════════════════════════════════════════════════════════════╝

Para: {user[1]}
Asunto: 🔐 Recuperación de contraseña - CoachBodyFit360

Hola {user[2]},

Has solicitado recuperar tu contraseña en CoachBodyFit360.

Para crear una nueva contraseña, haz clic en el siguiente enlace:
{reset_url}

Este enlace es válido por 1 hora.

Si no solicitaste este cambio, ignora este email.

---
CoachBodyFit360
Tu entrenador personal con IA
            """)
            
            print("\n" + "="*70)
            print("✅ TEST COMPLETADO")
            print("="*70)
            print(f"\n💡 Puedes usar este link para resetear la contraseña:")
            print(f"   {reset_url}")
            print("="*70)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("🧪 TEST: Sistema de Recuperación de Contraseñas (Railway)")
        print("="*70)
        print("\nUso: python test_password_reset_railway.py <email>")
        print("\nEjemplos:")
        print("  python test_password_reset_railway.py xxzeus16@hotmail.com")
        print("  python test_password_reset_railway.py ptecherasosa@icloud.com")
        print("="*70)
        return
    
    email = sys.argv[1]
    test_password_reset(email)

if __name__ == "__main__":
    main()
