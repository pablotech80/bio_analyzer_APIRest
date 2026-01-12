from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Multi-tenant architecture: Users belong to Organizations via Membership.
    """
    
    # Additional fields beyond AbstractUser
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone Number")
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Date of Birth")
    )
    
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', _('Male')),
            ('female', _('Female')),
            ('other', _('Other')),
        ],
        blank=True,
        null=True,
        verbose_name=_("Gender")
    )
    
    # Email verification
    email_verified = models.BooleanField(
        default=False,
        verbose_name=_("Email Verified")
    )
    
    email_verified_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Email Verified At")
    )
    
    # Profile
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name=_("Avatar")
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Biography")
    )
    
    # Timestamps (AbstractUser already has date_joined)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("Last Login IP")
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        """Return full name or username as fallback."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
