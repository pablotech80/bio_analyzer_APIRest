"""
Seed script for initial data: Permissions, Roles, and SuperAdmin user.

Run with: python manage.py shell < scripts/seed_initial_data.py
Or: python manage.py runscript seed_initial_data (if django-extensions is installed)
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.permissions.models import Permission, Role
from apps.organizations.models import Organization, Membership

User = get_user_model()


def create_permissions():
    """Create all system permissions."""
    permissions_data = [
        # BioAnalyze permissions
        {'name': 'bioanalyze.view_own', 'module': 'bioanalyze', 'action': 'view_own', 
         'description': 'View own biometric analyses'},
        {'name': 'bioanalyze.view_all', 'module': 'bioanalyze', 'action': 'view_all', 
         'description': 'View all biometric analyses in organization'},
        {'name': 'bioanalyze.create', 'module': 'bioanalyze', 'action': 'create', 
         'description': 'Create biometric analyses'},
        {'name': 'bioanalyze.update_own', 'module': 'bioanalyze', 'action': 'update_own', 
         'description': 'Update own biometric analyses'},
        {'name': 'bioanalyze.update_all', 'module': 'bioanalyze', 'action': 'update_all', 
         'description': 'Update all biometric analyses in organization'},
        {'name': 'bioanalyze.delete_own', 'module': 'bioanalyze', 'action': 'delete_own', 
         'description': 'Delete own biometric analyses'},
        {'name': 'bioanalyze.delete_all', 'module': 'bioanalyze', 'action': 'delete_all', 
         'description': 'Delete all biometric analyses in organization'},
        
        # Nutrition permissions
        {'name': 'nutrition.view_own', 'module': 'nutrition', 'action': 'view_own', 
         'description': 'View own nutrition plans'},
        {'name': 'nutrition.view_all', 'module': 'nutrition', 'action': 'view_all', 
         'description': 'View all nutrition plans in organization'},
        {'name': 'nutrition.create', 'module': 'nutrition', 'action': 'create', 
         'description': 'Create nutrition plans'},
        {'name': 'nutrition.update_own', 'module': 'nutrition', 'action': 'update_own', 
         'description': 'Update own nutrition plans'},
        {'name': 'nutrition.update_all', 'module': 'nutrition', 'action': 'update_all', 
         'description': 'Update all nutrition plans in organization'},
        {'name': 'nutrition.delete_own', 'module': 'nutrition', 'action': 'delete_own', 
         'description': 'Delete own nutrition plans'},
        {'name': 'nutrition.delete_all', 'module': 'nutrition', 'action': 'delete_all', 
         'description': 'Delete all nutrition plans in organization'},
        
        # Training permissions
        {'name': 'training.view_own', 'module': 'training', 'action': 'view_own', 
         'description': 'View own training plans'},
        {'name': 'training.view_all', 'module': 'training', 'action': 'view_all', 
         'description': 'View all training plans in organization'},
        {'name': 'training.create', 'module': 'training', 'action': 'create', 
         'description': 'Create training plans'},
        {'name': 'training.update_own', 'module': 'training', 'action': 'update_own', 
         'description': 'Update own training plans'},
        {'name': 'training.update_all', 'module': 'training', 'action': 'update_all', 
         'description': 'Update all training plans in organization'},
        {'name': 'training.delete_own', 'module': 'training', 'action': 'delete_own', 
         'description': 'Delete own training plans'},
        {'name': 'training.delete_all', 'module': 'training', 'action': 'delete_all', 
         'description': 'Delete all training plans in organization'},
        
        # User management permissions
        {'name': 'users.view_own', 'module': 'users', 'action': 'view_own', 
         'description': 'View own profile'},
        {'name': 'users.view_all', 'module': 'users', 'action': 'view_all', 
         'description': 'View all users in organization'},
        {'name': 'users.update_own', 'module': 'users', 'action': 'update_own', 
         'description': 'Update own profile'},
        {'name': 'users.update_all', 'module': 'users', 'action': 'update_all', 
         'description': 'Update all users in organization'},
        {'name': 'users.invite', 'module': 'users', 'action': 'invite', 
         'description': 'Invite users to organization'},
        {'name': 'users.remove', 'module': 'users', 'action': 'remove', 
         'description': 'Remove users from organization'},
        
        # Organization permissions
        {'name': 'organization.view', 'module': 'organization', 'action': 'view', 
         'description': 'View organization details'},
        {'name': 'organization.update', 'module': 'organization', 'action': 'update', 
         'description': 'Update organization settings'},
        {'name': 'organization.manage_members', 'module': 'organization', 'action': 'manage_members', 
         'description': 'Manage organization members'},
        {'name': 'organization.manage_roles', 'module': 'organization', 'action': 'manage_roles', 
         'description': 'Manage organization roles'},
        
        # System permissions
        {'name': 'system.admin', 'module': 'system', 'action': 'admin', 
         'description': 'Full system administration access'},
    ]
    
    created_count = 0
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            name=perm_data['name'],
            defaults={
                'module': perm_data['module'],
                'action': perm_data['action'],
                'description': perm_data['description']
            }
        )
        if created:
            created_count += 1
            print(f"✓ Created permission: {permission.name}")
    
    print(f"\n✅ Permissions: {created_count} created, {len(permissions_data) - created_count} already existed")
    return Permission.objects.all()


def create_roles(permissions):
    """Create system roles with appropriate permissions."""
    
    # Client Role
    client_role, created = Role.objects.get_or_create(
        name='Client',
        defaults={
            'description': 'Basic user with access to own data',
            'is_system_role': True
        }
    )
    if created:
        client_permissions = permissions.filter(action__in=['view_own', 'update_own', 'create'])
        client_role.permissions.set(client_permissions)
        print(f"✓ Created role: Client with {client_permissions.count()} permissions")
    
    # Trainer Role
    trainer_role, created = Role.objects.get_or_create(
        name='Trainer',
        defaults={
            'description': 'Personal trainer with access to manage clients',
            'is_system_role': True
        }
    )
    if created:
        trainer_permissions = permissions.exclude(module='system').exclude(action='delete_all')
        trainer_role.permissions.set(trainer_permissions)
        print(f"✓ Created role: Trainer with {trainer_permissions.count()} permissions")
    
    # Nutritionist Role
    nutritionist_role, created = Role.objects.get_or_create(
        name='Nutritionist',
        defaults={
            'description': 'Nutritionist with focus on nutrition plans',
            'is_system_role': True
        }
    )
    if created:
        nutritionist_permissions = permissions.filter(
            module__in=['nutrition', 'bioanalyze', 'users', 'organization']
        ).exclude(action='delete_all')
        nutritionist_role.permissions.set(nutritionist_permissions)
        print(f"✓ Created role: Nutritionist with {nutritionist_permissions.count()} permissions")
    
    # Admin Role
    admin_role, created = Role.objects.get_or_create(
        name='Admin',
        defaults={
            'description': 'Organization administrator with full access',
            'is_system_role': True
        }
    )
    if created:
        admin_permissions = permissions.exclude(name='system.admin')
        admin_role.permissions.set(admin_permissions)
        print(f"✓ Created role: Admin with {admin_permissions.count()} permissions")
    
    # SuperAdmin Role
    superadmin_role, created = Role.objects.get_or_create(
        name='SuperAdmin',
        defaults={
            'description': 'System-wide administrator with all permissions',
            'is_system_role': True
        }
    )
    if created:
        superadmin_role.permissions.set(permissions)
        print(f"✓ Created role: SuperAdmin with {permissions.count()} permissions")
    
    print(f"\n✅ Roles: 5 system roles configured")
    return {
        'client': client_role,
        'trainer': trainer_role,
        'nutritionist': nutritionist_role,
        'admin': admin_role,
        'superadmin': superadmin_role
    }


def create_superadmin(roles):
    """Create SuperAdmin user and organization."""
    
    # Check if SuperAdmin already exists
    if User.objects.filter(email='admin@coachbodyfit360.com').exists():
        print("\n⚠️  SuperAdmin user already exists")
        return
    
    # Create SuperAdmin organization
    org, created = Organization.objects.get_or_create(
        slug='coachbodyfit360-system',
        defaults={
            'name': 'CoachBodyFit360 System',
            'type': 'corporate',
            'description': 'System organization for platform administration',
            'subscription_plan': 'business',
            'is_active': True
        }
    )
    if created:
        print(f"✓ Created organization: {org.name}")
    
    # Create SuperAdmin user
    superadmin = User.objects.create_superuser(
        username='superadmin',
        email='admin@coachbodyfit360.com',
        password='Admin123!',  # Change this in production!
        first_name='Super',
        last_name='Admin',
        email_verified=True
    )
    print(f"✓ Created SuperAdmin user: {superadmin.email}")
    
    # Create membership
    membership = Membership.objects.create(
        user=superadmin,
        organization=org,
        role=roles['superadmin'],
        is_active=True
    )
    print(f"✓ Created membership: {superadmin.email} → {org.name}")
    
    print("\n" + "="*60)
    print("🎉 SUPERADMIN CREDENTIALS")
    print("="*60)
    print(f"Email:    admin@coachbodyfit360.com")
    print(f"Password: Admin123!")
    print(f"⚠️  IMPORTANT: Change this password immediately in production!")
    print("="*60)


def main():
    """Main seeding function."""
    print("\n" + "="*60)
    print("🌱 SEEDING INITIAL DATA")
    print("="*60 + "\n")
    
    print("📋 Step 1: Creating Permissions...")
    permissions = create_permissions()
    
    print("\n👥 Step 2: Creating Roles...")
    roles = create_roles(permissions)
    
    print("\n🔐 Step 3: Creating SuperAdmin...")
    create_superadmin(roles)
    
    print("\n" + "="*60)
    print("✅ SEEDING COMPLETED SUCCESSFULLY")
    print("="*60)
    print("\nYou can now:")
    print("1. Run the Django server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. Login with SuperAdmin credentials")
    print("\n")


if __name__ == '__main__':
    main()
