from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin for Permissions."""
    
    list_display = [
        'name',
        'module',
        'action',
        'created_at',
    ]
    
    list_filter = [
        'module',
        'action',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'description',
        'module',
        'action',
    ]
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        (_('Classification'), {
            'fields': ('module', 'action')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin for Roles with permission management."""
    
    list_display = [
        'name',
        'is_system_role',
        'permission_count',
        'created_at',
    ]
    
    list_filter = [
        'is_system_role',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'description',
    ]
    
    filter_horizontal = ['permissions']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_system_role')
        }),
        (_('Permissions'), {
            'fields': ('permissions',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def permission_count(self, obj):
        """Display number of permissions assigned to role."""
        return obj.permissions.count()
    
    permission_count.short_description = _('Permissions')
