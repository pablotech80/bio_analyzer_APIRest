# scripts/init_roles.py
"""
Script para inicializar roles y permisos en la base de datos.
Ejecutar después de crear las tablas con flask db upgrade.
"""
from app import create_app, db
from app.models.user import Permission, Role


def init_roles_and_permissions():
    """Crear roles y permisos por defecto."""
    app = create_app("development")

    with app.app_context():
        print("🔄 Inicializando roles y permisos...")

        # Definir permisos
        permissions_data = [
            # Permisos de perfil
            ("read:own_profile", "Ver propio perfil"),
            ("write:own_profile", "Editar propio perfil"),
            # Permisos de análisis biométricos
            ("read:own_analyses", "Ver propios análisis"),
            ("write:own_analyses", "Crear propios análisis"),
            # Permisos de planes
            ("read:own_plans", "Ver propios planes"),
            ("write:own_plans", "Crear propios planes"),
            # Permisos de progreso
            ("read:own_progress", "Ver propio progreso"),
            ("write:own_progress", "Registrar propio progreso"),
            # Permisos de clientes (trainer/nutritionist)
            ("read:clients", "Ver clientes asignados"),
            ("write:clients", "Editar información de clientes"),
            ("read:client_data", "Ver datos de clientes"),
            ("write:client_notes", "Agregar notas a clientes"),
            # Permisos de planes de entrenamiento (trainer)
            ("write:training_plans", "Crear planes de entrenamiento"),
            ("assign:training_plans", "Asignar planes de entrenamiento"),
            # Permisos de planes nutricionales (nutritionist)
            ("write:nutrition_plans", "Crear planes nutricionales"),
            ("assign:nutrition_plans", "Asignar planes nutricionales"),
            # Permisos de administrador
            ("admin:all", "Acceso total al sistema"),
            ("read:all_users", "Ver todos los usuarios"),
            ("write:all_users", "Editar cualquier usuario"),
            ("delete:users", "Eliminar usuarios"),
            ("manage:roles", "Gestionar roles y permisos"),
        ]

        # Crear permisos si no existen
        permissions = {}
        for perm_name, perm_desc in permissions_data:
            perm = Permission.query.filter_by(name=perm_name).first()
            if not perm:
                perm = Permission(name=perm_name, description=perm_desc)
                db.session.add(perm)
                print(f"  ✅ Permiso creado: {perm_name}")
            permissions[perm_name] = perm

        db.session.commit()

        # Definir roles con sus permisos
        roles_data = {
            "client": {
                "description": "Usuario cliente estándar",
                "permissions": [
                    "read:own_profile",
                    "write:own_profile",
                    "read:own_analyses",
                    "write:own_analyses",
                    "read:own_plans",
                    "read:own_progress",
                    "write:own_progress",
                ],
            },
            "trainer": {
                "description": "Entrenador personal",
                "permissions": [
                    "read:own_profile",
                    "write:own_profile",
                    "read:own_analyses",
                    "write:own_analyses",
                    "read:own_plans",
                    "read:own_progress",
                    "write:own_progress",
                    "read:clients",
                    "write:clients",
                    "read:client_data",
                    "write:client_notes",
                    "write:training_plans",
                    "assign:training_plans",
                ],
            },
            "nutritionist": {
                "description": "Nutricionista/Dietista",
                "permissions": [
                    "read:own_profile",
                    "write:own_profile",
                    "read:own_analyses",
                    "write:own_analyses",
                    "read:own_plans",
                    "read:own_progress",
                    "write:own_progress",
                    "read:clients",
                    "write:clients",
                    "read:client_data",
                    "write:client_notes",
                    "write:nutrition_plans",
                    "assign:nutrition_plans",
                ],
            },
            "admin": {
                "description": "Administrador del sistema",
                "permissions": [
                    "admin:all",
                    "read:all_users",
                    "write:all_users",
                    "delete:users",
                    "manage:roles",
                    # Admin tiene acceso a todo, pero listamos explícitos
                    "read:own_profile",
                    "write:own_profile",
                    "read:own_analyses",
                    "write:own_analyses",
                    "read:clients",
                    "write:clients",
                    "read:client_data",
                    "write:training_plans",
                    "write:nutrition_plans",
                ],
            },
        }

        # Crear roles y asignar permisos
        for role_name, role_info in roles_data.items():
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=role_info["description"])
                db.session.add(role)
                print(f"  ✅ Rol creado: {role_name}")
            else:
                print(f"  ℹ️  Rol ya existe: {role_name}")

            # Asignar permisos al rol
            for perm_name in role_info["permissions"]:
                if perm_name in permissions:
                    if permissions[perm_name] not in role.permissions.all():
                        role.permissions.append(permissions[perm_name])

        db.session.commit()

        print("\n✅ Roles y permisos inicializados exitosamente!")
        print("\n📋 Resumen:")
        print(f"   - Total permisos: {Permission.query.count()}")
        print(f"   - Total roles: {Role.query.count()}")

        # Mostrar roles y sus permisos
        print("\n🔐 Roles configurados:")
        for role in Role.query.all():
            print(f"\n   {role.name.upper()}:")
            print(f"   - Descripción: {role.description}")
            print(f"   - Permisos: {role.permissions.count()}")


if __name__ == "__main__":
    init_roles_and_permissions()
