#!/usr/bin/env python3
"""
Script para resetear contraseña directamente (sin confirmación)
Uso: python reset_password_direct.py <email> <nueva_contraseña>
"""
import sys
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

RAILWAY_DB_URL = "postgresql://postgres:engtSRttlVTDiZYzPQkRiFrnuRdgaVzg@centerbeam.proxy.rlwy.net:57147/railway"

def reset_password(email, new_password):
    """Resetea la contraseña de un usuario"""
    try:
        engine = create_engine(RAILWAY_DB_URL, echo=False)
        
        # Generar hash de la contraseña (mismo método que usa Flask-Bcrypt)
        password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        with engine.connect() as conn:
            # Verificar que el usuario existe
            result = conn.execute(
                text("SELECT id, email, first_name, last_name FROM users WHERE email = :email"),
                {"email": email}
            )
            user = result.fetchone()
            
            if not user:
                print(f"❌ Usuario con email '{email}' no encontrado.")
                return False
            
            print(f"\n✅ Usuario encontrado:")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Nombre: {user[2]} {user[3]}")
            
            # Actualizar contraseña
            conn.execute(
                text("UPDATE users SET password_hash = :password_hash WHERE email = :email"),
                {"password_hash": password_hash, "email": email}
            )
            conn.commit()
            
            print(f"\n✅ CONTRASEÑA ACTUALIZADA EXITOSAMENTE!")
            print(f"\n📧 Email: {email}")
            print(f"🔑 Nueva contraseña: {new_password}")
            print(f"\n💡 El usuario puede iniciar sesión ahora con estas credenciales.")
            return True
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("="*70)
        print("🔐 RESETEAR CONTRASEÑA DE USUARIO")
        print("="*70)
        print("\nUso: python reset_password_direct.py <email> <nueva_contraseña>")
        print("\nEjemplos:")
        print('  python reset_password_direct.py xxzeus16@hotmail.com "NuevaPass123"')
        print('  python reset_password_direct.py test@mvp.com "TempPass2024"')
        print("\n⚠️  IMPORTANTE: La contraseña debe estar entre comillas si tiene espacios")
        print("="*70)
        return
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    print("="*70)
    print("🔐 RESETEAR CONTRASEÑA - RAILWAY POSTGRESQL")
    print("="*70)
    
    reset_password(email, new_password)

if __name__ == "__main__":
    main()
