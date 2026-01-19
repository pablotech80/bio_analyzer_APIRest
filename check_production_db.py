#!/usr/bin/env python3
"""
Script para diagnosticar problemas de registro en producción.
Verifica el estado de la base de datos y configuración.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_database_connection():
    """Verificar conexión a la base de datos de producción."""
    print("=" * 60)
    print("DIAGNÓSTICO DE BASE DE DATOS - PRODUCCIÓN")
    print("=" * 60)
    
    # Verificar variables de entorno
    db_url = os.getenv('DATABASE_PRIVATE_URL') or os.getenv('DATABASE_URL')
    
    if not db_url:
        print("❌ ERROR: No hay DATABASE_URL configurado")
        return False
    
    print(f"✅ DATABASE_URL configurado: {db_url[:30]}...")
    
    # Intentar conectar
    try:
        from sqlalchemy import create_engine, text
        
        # Ajustar URL si es necesario
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Test básico
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a base de datos exitosa")
            
            # Verificar tabla users
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name = 'users'
            """))
            users_table_exists = result.fetchone()[0] > 0
            
            if users_table_exists:
                print("✅ Tabla 'users' existe")
                
                # Contar usuarios
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.fetchone()[0]
                print(f"📊 Total de usuarios: {user_count}")
            else:
                print("❌ ERROR: Tabla 'users' NO existe")
                return False
            
            # Verificar tabla roles
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name = 'roles'
            """))
            roles_table_exists = result.fetchone()[0] > 0
            
            if roles_table_exists:
                print("✅ Tabla 'roles' existe")
                
                # Verificar rol 'client'
                result = conn.execute(text("SELECT COUNT(*) FROM roles WHERE name = 'client'"))
                client_role_exists = result.fetchone()[0] > 0
                
                if client_role_exists:
                    print("✅ Rol 'client' existe")
                else:
                    print("⚠️  WARNING: Rol 'client' NO existe - esto causará errores de registro")
                    print("   Solución: Ejecutar init_db.py o crear el rol manualmente")
                
                # Listar todos los roles
                result = conn.execute(text("SELECT name, description FROM roles"))
                roles = result.fetchall()
                print(f"📊 Roles disponibles: {len(roles)}")
                for role in roles:
                    print(f"   - {role[0]}: {role[1]}")
            else:
                print("❌ ERROR: Tabla 'roles' NO existe")
                return False
            
            # Verificar constraints de email y username
            result = conn.execute(text("""
                SELECT constraint_name, constraint_type 
                FROM information_schema.table_constraints 
                WHERE table_name = 'users' 
                AND constraint_type IN ('UNIQUE', 'PRIMARY KEY')
            """))
            constraints = result.fetchall()
            print(f"📊 Constraints en tabla users: {len(constraints)}")
            for constraint in constraints:
                print(f"   - {constraint[0]}: {constraint[1]}")
            
            return True
            
    except Exception as e:
        print(f"❌ ERROR al conectar a la base de datos: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_environment_variables():
    """Verificar variables de entorno críticas."""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("=" * 60)
    
    critical_vars = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'DATABASE_PRIVATE_URL': os.getenv('DATABASE_PRIVATE_URL'),
        'FLASK_ENV': os.getenv('FLASK_ENV'),
    }
    
    for var_name, var_value in critical_vars.items():
        if var_value:
            display_value = var_value[:20] + "..." if len(var_value) > 20 else var_value
            print(f"✅ {var_name}: {display_value}")
        else:
            print(f"⚠️  {var_name}: NO CONFIGURADO")
    
    # Verificar configuración de email
    email_vars = {
        'MAIL_SERVER': os.getenv('MAIL_SERVER'),
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    }
    
    print("\n📧 Configuración de Email:")
    for var_name, var_value in email_vars.items():
        if var_value:
            if 'PASSWORD' in var_name:
                print(f"✅ {var_name}: ***")
            else:
                print(f"✅ {var_name}: {var_value}")
        else:
            print(f"⚠️  {var_name}: NO CONFIGURADO")


def test_user_creation():
    """Simular creación de usuario para detectar errores."""
    print("\n" + "=" * 60)
    print("TEST DE CREACIÓN DE USUARIO (SIMULACIÓN)")
    print("=" * 60)
    
    try:
        from app import create_app
        from app.models.user import User, Role
        from app import db
        
        app = create_app('production')
        
        with app.app_context():
            # Verificar que exista el rol client
            client_role = Role.query.filter_by(name='client').first()
            
            if not client_role:
                print("❌ ERROR CRÍTICO: Rol 'client' no existe en la base de datos")
                print("   Esto impedirá que los usuarios se registren")
                print("\n🔧 SOLUCIÓN:")
                print("   1. Ejecutar: python init_db.py")
                print("   2. O crear el rol manualmente en Railway")
                return False
            else:
                print(f"✅ Rol 'client' encontrado (ID: {client_role.id})")
            
            # Verificar usuarios existentes
            total_users = User.query.count()
            print(f"📊 Total de usuarios en BD: {total_users}")
            
            # Verificar últimos registros
            recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
            print(f"\n📋 Últimos 5 usuarios registrados:")
            for user in recent_users:
                print(f"   - {user.username} ({user.email}) - {user.created_at}")
            
            return True
            
    except Exception as e:
        print(f"❌ ERROR en test de creación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los diagnósticos."""
    print("\n🔍 INICIANDO DIAGNÓSTICO DE SISTEMA DE REGISTRO\n")
    
    # 1. Verificar variables de entorno
    check_environment_variables()
    
    # 2. Verificar conexión a BD
    db_ok = check_database_connection()
    
    if not db_ok:
        print("\n❌ FALLO EN CONEXIÓN A BASE DE DATOS")
        print("   No se pueden ejecutar más tests")
        return
    
    # 3. Test de creación de usuario
    test_ok = test_user_creation()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    if db_ok and test_ok:
        print("✅ Sistema aparentemente funcional")
        print("   Si los usuarios no pueden registrarse, revisar:")
        print("   1. Logs de Railway para errores específicos")
        print("   2. Configuración HTTPS/SSL")
        print("   3. CSRF tokens (SESSION_COOKIE_SECURE)")
    else:
        print("❌ PROBLEMAS DETECTADOS - Revisar errores arriba")
        print("\n🔧 ACCIONES RECOMENDADAS:")
        print("   1. Ejecutar migraciones: flask db upgrade")
        print("   2. Inicializar roles: python init_db.py")
        print("   3. Verificar variables de entorno en Railway")


if __name__ == '__main__':
    main()
