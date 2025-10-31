#!/usr/bin/env python3
"""
Script para verificar y actualizar permisos de admin
"""
import sys
sys.path.insert(0, '/Users/macbookpro/bio_analyzer_APIRest')

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("=" * 60)
    print("VERIFICACION DE USUARIOS ADMIN")
    print("=" * 60)
    
    # Listar todos los usuarios
    users = User.query.all()
    
    if not users:
        print("No hay usuarios en la base de datos")
    else:
        print(f"\nTotal usuarios: {len(users)}\n")
        for user in users:
            admin_status = "SI" if user.is_admin else "NO"
            print(f"- Email: {user.email}")
            print(f"  Admin: {admin_status}")
            print()
    
    # Preguntar si quiere hacer admin a alguien
    print("\nPara hacer admin a un usuario, ejecuta:")
    print("python check_admin.py EMAIL")
    
    # Si se pasa un email como argumento, hacerlo admin
    if len(sys.argv) > 1:
        email = sys.argv[1]
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"\n✅ Usuario {email} ahora es ADMIN!")
        else:
            print(f"\n❌ Usuario {email} no encontrado")
