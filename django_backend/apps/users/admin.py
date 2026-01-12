from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with additional fields."""
    
    list_display = [
        'email',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'email_verified',
        'date_joined',
    ]
    
    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verified',
        'gender',
        'date_joined',
    ]
    
    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
        'phone',
    ]
    
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'date_of_birth',
                'gender',
                'avatar',
                'bio',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Email Verification'), {
            'fields': ('email_verified', 'email_verified_at')
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined', 'updated_at')
        }),
        (_('Security'), {
            'fields': ('last_login_ip',)
        }),
    )
    
    readonly_fields = ['date_joined', 'updated_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )
