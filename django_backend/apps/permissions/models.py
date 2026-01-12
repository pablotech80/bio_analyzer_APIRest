from django.db import models
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    """
    Granular permissions for the system.
    
    Examples:
    - bioanalyze.view_own
    - bioanalyze.view_all
    - nutrition.create_plan
    - users.manage
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Permission Name"),
        help_text=_("Format: module.action (e.g., bioanalyze.view_own)")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    
    module = models.CharField(
        max_length=50,
        verbose_name=_("Module"),
        help_text=_("Module this permission belongs to (e.g., bioanalyze, nutrition)")
    )
    
    action = models.CharField(
        max_length=50,
        verbose_name=_("Action"),
        help_text=_("Action allowed (e.g., view_own, create, delete)")
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    
    class Meta:
        db_table = 'permissions'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        ordering = ['module', 'action']
        indexes = [
            models.Index(fields=['module', 'action']),
        ]
    
    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Roles group permissions together.
    
    Examples:
    - Client: Basic user with limited access
    - Trainer: Can manage clients and create plans
    - Admin: Full access to organization
    - SuperAdmin: System-wide access
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Role Name")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    
    permissions = models.ManyToManyField(
        Permission,
        related_name='roles',
        blank=True,
        verbose_name=_("Permissions")
    )
    
    # System roles cannot be deleted
    is_system_role = models.BooleanField(
        default=False,
        verbose_name=_("System Role"),
        help_text=_("System roles cannot be deleted")
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    class Meta:
        db_table = 'roles'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def has_permission(self, permission_name):
        """Check if role has a specific permission."""
        return self.permissions.filter(name=permission_name).exists()
