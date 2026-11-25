"""
doctors/admin.py — Admin Configuration for Doctor Model

Registers Doctor model in Django admin for administration and verification.
"""

from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin interface options for Doctor entity.
    """
    list_display = ('name', 'specialization', 'email', 'contact_number', 'years_of_experience', 'created_at')
    list_filter = ('specialization',)
    search_fields = ('name', 'email', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
