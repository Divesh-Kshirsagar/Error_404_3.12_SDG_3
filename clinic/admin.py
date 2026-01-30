from django.contrib import admin
from .models import Patient, Case


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone']
    list_filter = ['created_at']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['patient', 'risk_score', 'status', 'created_at']
    list_filter = ['status', 'risk_score', 'created_at']
    search_fields = ['patient__name', 'transcript']
    readonly_fields = ['symptoms', 'risk_score']
