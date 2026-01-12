from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    """
    Multi-tenant organization model.
    
    Each organization can be:
    - Individual user (personal account)
    - Gym/Fitness center
    - Nutritionist practice
    - Corporate wellness program
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name=_("Organization Name")
    )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("Slug")
    )
    
    type = models.CharField(
        max_length=50,
        choices=[
            ('individual', _('Individual')),
            ('gym', _('Gym/Fitness Center')),
            ('nutritionist', _('Nutritionist Practice')),
            ('trainer', _('Personal Trainer')),
            ('corporate', _('Corporate')),
        ],
        default='individual',
        verbose_name=_("Organization Type")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    
    logo = models.ImageField(
        upload_to='organizations/logos/',
        blank=True,
        null=True,
        verbose_name=_("Logo")
    )
    
    # Contact information
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Contact Email")
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Contact Phone")
    )
    
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Website")
    )
    
    # Address
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Address")
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("City")
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Country")
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    
    # Subscription (future)
    subscription_plan = models.CharField(
        max_length=50,
        choices=[
            ('free', _('Free')),
            ('premium', _('Premium')),
            ('pro', _('Pro')),
            ('business', _('Business')),
        ],
        default='free',
        verbose_name=_("Subscription Plan")
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
        db_table = 'organizations'
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Membership(models.Model):
    """
    Links Users to Organizations with specific Roles.
    
    A user can belong to multiple organizations with different roles.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_("User")
    )
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_("Organization")
    )
    
    role = models.ForeignKey(
        'permissions.Role',
        on_delete=models.PROTECT,
        related_name='memberships',
        verbose_name=_("Role")
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    
    # Invitation tracking
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invitations',
        verbose_name=_("Invited By")
    )
    
    invited_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Invited At")
    )
    
    accepted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Accepted At")
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
        db_table = 'memberships'
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')
        unique_together = [['user', 'organization']]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role.name})"
