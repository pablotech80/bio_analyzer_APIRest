from django.contrib import admin
from .models import TrainingPlan


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'title']
    autocomplete_fields = ['user', 'organization', 'biometric_analysis']
    readonly_fields = ['created_at', 'updated_at']
