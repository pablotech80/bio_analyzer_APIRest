from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainingPlan(models.Model):
    """Training plan for a user."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_plans',
        verbose_name=_("User")
    )
    
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='training_plans',
        verbose_name=_("Organization")
    )
    
    biometric_analysis = models.ForeignKey(
        'bioanalyze.BiometricAnalysis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='training_plans',
        verbose_name=_("Biometric Analysis")
    )
    
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    
    # Plan data (JSON)
    plan_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Plan Data"),
        help_text=_("Detailed workout routines, exercises, and progressions")
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        db_table = 'training_plans'
        verbose_name = _('Training Plan')
        verbose_name_plural = _('Training Plans')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
