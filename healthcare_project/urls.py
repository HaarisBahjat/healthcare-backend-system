"""
healthcare_project URL Configuration

Root URL router for the Healthcare Backend API.
Each app defines its own urls.py; they are included here under a versioned
API namespace so the URL structure stays clean and organized.

URL Structure:
    /api/auth/      → accounts app (register, login, token refresh)
    /api/patients/  → patients app (CRUD)
    /api/doctors/   → doctors app (CRUD)
    /api/mappings/  → mappings app (patient-doctor assignments)
    /admin/         → Django admin interface
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel — useful for direct DB inspection during development
    path('admin/', admin.site.urls),

    # --- API Endpoints ---
    # Each app registers its own URL patterns via include()
    # Why include(): Keeps URL definitions modular — each app owns its routes

    path('api/auth/', include('accounts.urls')),       # Authentication routes
    path('api/patients/', include('patients.urls')),    # Patient management routes
    path('api/doctors/', include('doctors.urls')),      # Doctor management routes
    path('api/mappings/', include('mappings.urls')),    # Patient-Doctor mapping routes
]
