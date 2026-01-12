from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class NutritionPlan(models.Model):
    """Nutrition plan for a user."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='nutrition_plans',
        verbose_name=_("User")
    )
    
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='nutrition_plans',
        verbose_name=_("Organization")
    )
    
    biometric_analysis = models.ForeignKey(
        'bioanalyze.BiometricAnalysis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nutrition_plans',
        verbose_name=_("Biometric Analysis")
    )
    
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    
    # Macros
    daily_calories = models.FloatField(verbose_name=_("Daily Calories"))
    protein_grams = models.FloatField(verbose_name=_("Protein (g)"))
    carbs_grams = models.FloatField(verbose_name=_("Carbs (g)"))
    fats_grams = models.FloatField(verbose_name=_("Fats (g)"))
    
    # Plan data (JSON)
    plan_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Plan Data"),
        help_text=_("Detailed meal plan, recipes, and recommendations")
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        db_table = 'nutrition_plans'
        verbose_name = _('Nutrition Plan')
        verbose_name_plural = _('Nutrition Plans')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
