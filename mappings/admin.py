"""
mappings/admin.py — Admin Configuration for PatientDoctorMapping
"""

from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient-Doctor Mapping.
    """
    list_display = ('id', 'patient', 'doctor', 'assigned_at')
    list_filter = ('doctor', 'assigned_at')
    search_fields = ('patient__name', 'doctor__name')
    readonly_fields = ('assigned_at',)
    ordering = ('-assigned_at',)
