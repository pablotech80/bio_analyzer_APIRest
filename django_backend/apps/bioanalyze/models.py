from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BiometricAnalysis(models.Model):
    """
    Biometric analysis snapshot for a user.
    
    Stores raw input data, calculated metrics, and FitMaster AI interpretation.
    """
    
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', _('Sedentary')),
        ('light', _('Light')),
        ('moderate', _('Moderate')),
        ('active', _('Active')),
        ('very_active', _('Very Active')),
    ]
    
    GOAL_CHOICES = [
        ('lose_weight', _('Lose Weight')),
        ('maintain', _('Maintain')),
        ('gain_muscle', _('Gain Muscle')),
    ]
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='biometric_analyses',
        verbose_name=_("User")
    )
    
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='biometric_analyses',
        verbose_name=_("Organization")
    )
    
    # Input data (required)
    weight = models.FloatField(verbose_name=_("Weight (kg)"))
    height = models.FloatField(verbose_name=_("Height (cm)"))
    age = models.IntegerField(verbose_name=_("Age"))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    
    # Circumferences
    neck = models.FloatField(verbose_name=_("Neck (cm)"))
    waist = models.FloatField(verbose_name=_("Waist (cm)"))
    hip = models.FloatField(null=True, blank=True, verbose_name=_("Hip (cm)"))
    
    # Bilateral muscle measurements (optional)
    biceps_left = models.FloatField(null=True, blank=True, verbose_name=_("Left Biceps (cm)"))
    biceps_right = models.FloatField(null=True, blank=True, verbose_name=_("Right Biceps (cm)"))
    thigh_left = models.FloatField(null=True, blank=True, verbose_name=_("Left Thigh (cm)"))
    thigh_right = models.FloatField(null=True, blank=True, verbose_name=_("Right Thigh (cm)"))
    calf_left = models.FloatField(null=True, blank=True, verbose_name=_("Left Calf (cm)"))
    calf_right = models.FloatField(null=True, blank=True, verbose_name=_("Right Calf (cm)"))
    
    # Activity data
    activity_factor = models.FloatField(null=True, blank=True, verbose_name=_("Activity Factor"))
    activity_level = models.CharField(
        max_length=32,
        choices=ACTIVITY_LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Activity Level")
    )
    goal = models.CharField(
        max_length=32,
        choices=GOAL_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Goal")
    )
    
    # Calculated metrics
    bmi = models.FloatField(null=True, blank=True, verbose_name=_("BMI"))
    bmr = models.FloatField(null=True, blank=True, verbose_name=_("BMR"))
    tdee = models.FloatField(null=True, blank=True, verbose_name=_("TDEE"))
    body_fat_percentage = models.FloatField(null=True, blank=True, verbose_name=_("Body Fat %"))
    lean_mass = models.FloatField(null=True, blank=True, verbose_name=_("Lean Mass (kg)"))
    fat_mass = models.FloatField(null=True, blank=True, verbose_name=_("Fat Mass (kg)"))
    ffmi = models.FloatField(null=True, blank=True, verbose_name=_("FFMI"))
    body_water = models.FloatField(null=True, blank=True, verbose_name=_("Body Water %"))
    waist_hip_ratio = models.FloatField(null=True, blank=True, verbose_name=_("WHR"))
    waist_height_ratio = models.FloatField(null=True, blank=True, verbose_name=_("WHtR"))
    metabolic_age = models.FloatField(null=True, blank=True, verbose_name=_("Metabolic Age"))
    
    # Nutrition targets
    maintenance_calories = models.FloatField(null=True, blank=True, verbose_name=_("Maintenance Calories"))
    protein_grams = models.FloatField(null=True, blank=True, verbose_name=_("Protein (g)"))
    carbs_grams = models.FloatField(null=True, blank=True, verbose_name=_("Carbs (g)"))
    fats_grams = models.FloatField(null=True, blank=True, verbose_name=_("Fats (g)"))
    
    # FitMaster AI data (consolidated JSON)
    fitmaster_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("FitMaster AI Data"),
        help_text=_("Complete AI interpretation, nutrition plan, and training plan")
    )
    
    # Photo URLs (Azure Blob Storage)
    front_photo_url = models.URLField(null=True, blank=True, verbose_name=_("Front Photo"))
    back_photo_url = models.URLField(null=True, blank=True, verbose_name=_("Back Photo"))
    side_photo_url = models.URLField(null=True, blank=True, verbose_name=_("Side Photo"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        db_table = 'biometric_analyses'
        verbose_name = _('Biometric Analysis')
        verbose_name_plural = _('Biometric Analyses')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['organization', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def has_fitmaster_analysis(self):
        """Check if FitMaster AI has processed this analysis."""
        return self.fitmaster_data is not None and bool(self.fitmaster_data)
    
    @property
    def biceps_average(self):
        """Calculate average biceps circumference."""
        if self.biceps_left and self.biceps_right:
            return round((self.biceps_left + self.biceps_right) / 2, 2)
        return self.biceps_left or self.biceps_right
    
    @property
    def thigh_average(self):
        """Calculate average thigh circumference."""
        if self.thigh_left and self.thigh_right:
            return round((self.thigh_left + self.thigh_right) / 2, 2)
        return self.thigh_left or self.thigh_right
    
    @property
    def calf_average(self):
        """Calculate average calf circumference."""
        if self.calf_left and self.calf_right:
            return round((self.calf_left + self.calf_right) / 2, 2)
        return self.calf_left or self.calf_right
