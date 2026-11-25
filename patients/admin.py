"""
patients/admin.py — Admin Configuration for Patient Model

Registers the Patient model with Django's admin interface for
easy browsing, searching, and managing patient records during development.
"""

from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Patient model.

    list_display: Columns shown in the patient list view.
    list_filter: Sidebar filters for quick filtering by gender or creator.
    search_fields: Fields searchable from the admin search bar.
    readonly_fields: Fields that cannot be edited in the admin form
                     (auto-managed by the system).
    ordering: Default sort order in the admin list.
    """
    list_display = ('name', 'date_of_birth', 'gender', 'contact_number', 'created_by', 'created_at')
    list_filter = ('gender', 'created_by')
    search_fields = ('name', 'contact_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
