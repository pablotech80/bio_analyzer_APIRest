from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import BiometricAnalysis


@admin.register(BiometricAnalysis)
class BiometricAnalysisAdmin(admin.ModelAdmin):
    """Admin for Biometric Analyses."""
    
    list_display = [
        'user',
        'organization',
        'weight',
        'height',
        'bmi',
        'body_fat_percentage',
        'has_fitmaster_analysis',
        'created_at',
    ]
    
    list_filter = [
        'gender',
        'activity_level',
        'goal',
        'created_at',
    ]
    
    search_fields = [
        'user__email',
        'user__username',
        'organization__name',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['user', 'organization']
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user', 'organization')
        }),
        (_('Basic Measurements'), {
            'fields': ('weight', 'height', 'age', 'gender')
        }),
        (_('Circumferences'), {
            'fields': ('neck', 'waist', 'hip')
        }),
        (_('Bilateral Measurements'), {
            'fields': (
                ('biceps_left', 'biceps_right'),
                ('thigh_left', 'thigh_right'),
                ('calf_left', 'calf_right'),
            ),
            'classes': ('collapse',)
        }),
        (_('Activity & Goals'), {
            'fields': ('activity_level', 'activity_factor', 'goal')
        }),
        (_('Calculated Metrics'), {
            'fields': (
                'bmi',
                'bmr',
                'tdee',
                'body_fat_percentage',
                'lean_mass',
                'fat_mass',
                'ffmi',
                'body_water',
                'waist_hip_ratio',
                'waist_height_ratio',
                'metabolic_age',
            ),
            'classes': ('collapse',)
        }),
        (_('Nutrition Targets'), {
            'fields': (
                'maintenance_calories',
                'protein_grams',
                'carbs_grams',
                'fats_grams',
            ),
            'classes': ('collapse',)
        }),
        (_('Photos'), {
            'fields': ('front_photo_url', 'back_photo_url', 'side_photo_url'),
            'classes': ('collapse',)
        }),
        (_('FitMaster AI'), {
            'fields': ('fitmaster_data',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_fitmaster_analysis(self, obj):
        """Display if analysis has FitMaster AI data."""
        return obj.has_fitmaster_analysis
    
    has_fitmaster_analysis.boolean = True
    has_fitmaster_analysis.short_description = _('Has AI Analysis')
