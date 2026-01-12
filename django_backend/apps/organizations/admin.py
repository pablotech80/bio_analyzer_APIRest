from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Organization, Membership


class MembershipInline(admin.TabularInline):
    """Inline for managing memberships within Organization admin."""
    model = Membership
    extra = 1
    autocomplete_fields = ['user', 'role']
    readonly_fields = ['invited_at', 'accepted_at', 'created_at']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin for Organizations with inline memberships."""
    
    list_display = [
        'name',
        'type',
        'subscription_plan',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'type',
        'subscription_plan',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'slug',
        'email',
        'city',
        'country',
    ]
    
    prepopulated_fields = {'slug': ('name',)}
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'type', 'description', 'logo')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'website')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'country')
        }),
        (_('Subscription'), {
            'fields': ('subscription_plan', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Admin for Memberships."""
    
    list_display = [
        'user',
        'organization',
        'role',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'role',
        'created_at',
    ]
    
    search_fields = [
        'user__email',
        'user__username',
        'organization__name',
    ]
    
    autocomplete_fields = ['user', 'organization', 'role', 'invited_by']
    
    readonly_fields = ['invited_at', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'organization', 'role', 'is_active')
        }),
        (_('Invitation'), {
            'fields': ('invited_by', 'invited_at', 'accepted_at')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
