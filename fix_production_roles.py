#!/usr/bin/env python3
"""
Script para crear roles faltantes en producción.
Ejecutar si los usuarios no pueden registrarse por falta de rol 'client'.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def create_missing_roles():
    """Crear roles necesarios en la base de datos."""
    print("=" * 60)
    print("CREANDO ROLES FALTANTES EN PRODUCCIÓN")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models.user import Role
        
        # Usar configuración de producción
        app = create_app('production')
        
        with app.app_context():
            # Roles necesarios
            required_roles = [
                {'name': 'client', 'description': 'Usuario cliente estándar'},
                {'name': 'admin', 'description': 'Administrador del sistema'},
                {'name': 'trainer', 'description': 'Entrenador personal'},
            ]
            
            created_count = 0
            
            for role_data in required_roles:
                existing_role = Role.query.filter_by(name=role_data['name']).first()
                
                if existing_role:
                    print(f"✅ Rol '{role_data['name']}' ya existe (ID: {existing_role.id})")
                else:
                    new_role = Role(
                        name=role_data['name'],
                        description=role_data['description']
                    )
                    db.session.add(new_role)
                    created_count += 1
                    print(f"➕ Creando rol '{role_data['name']}'...")
            
            if created_count > 0:
                db.session.commit()
                print(f"\n✅ {created_count} roles creados exitosamente")
            else:
                print("\n✅ Todos los roles ya existen")
            
            # Verificar roles finales
            all_roles = Role.query.all()
            print(f"\n📊 Total de roles en sistema: {len(all_roles)}")
            for role in all_roles:
                print(f"   - {role.name}: {role.description}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = create_missing_roles()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ ROLES CONFIGURADOS CORRECTAMENTE")
        print("   Los usuarios ahora deberían poder registrarse")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ ERROR AL CONFIGURAR ROLES")
        print("   Contacta al administrador del sistema")
        print("=" * 60)
