#!/usr/bin/env python3
"""
Script para resetear contraseña de un usuario en Railway PostgreSQL
Uso: python reset_password.py <email> <nueva_contraseña>
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
                return
            
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
            
            print(f"\n✅ Contraseña actualizada exitosamente!")
            print(f"   Nueva contraseña: {new_password}")
            print(f"\n📝 El usuario puede iniciar sesión con:")
            print(f"   Email: {email}")
            print(f"   Contraseña: {new_password}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    if len(sys.argv) < 3:
        print("="*70)
        print("🔐 RESETEAR CONTRASEÑA DE USUARIO")
        print("="*70)
        print("\nUso: python reset_password.py <email> <nueva_contraseña>")
        print("\nEjemplos:")
        print('  python reset_password.py xxzeus16@hotmail.com "NuevaPass123"')
        print('  python reset_password.py test@mvp.com "TempPass2024"')
        print("\n⚠️  IMPORTANTE: La contraseña debe estar entre comillas si tiene espacios")
        print("="*70)
        return
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    print("="*70)
    print("🔐 RESETEAR CONTRASEÑA")
    print("="*70)
    
    # Confirmar acción
    print(f"\n⚠️  Vas a cambiar la contraseña de: {email}")
    print(f"   Nueva contraseña: {new_password}")
    confirm = input("\n¿Continuar? (s/n): ").strip().lower()
    
    if confirm == 's' or confirm == 'si':
        reset_password(email, new_password)
    else:
        print("\n❌ Operación cancelada.")

if __name__ == "__main__":
    main()
