"""
patients/urls.py — Patient Management URL Routes

Uses DRF's DefaultRouter to automatically generate URL patterns
from the PatientViewSet.

Why DefaultRouter?
- ModelViewSet defines all CRUD actions (list, create, retrieve, update, destroy).
- The router inspects the ViewSet and auto-creates URL patterns for each action:
    GET    /api/patients/        → PatientViewSet.list()
    POST   /api/patients/        → PatientViewSet.create()
    GET    /api/patients/<pk>/   → PatientViewSet.retrieve()
    PUT    /api/patients/<pk>/   → PatientViewSet.update()
    PATCH  /api/patients/<pk>/   → PatientViewSet.partial_update()
    DELETE /api/patients/<pk>/   → PatientViewSet.destroy()
- This eliminates the need to manually write 6 separate path() entries.

Note: The base prefix '/api/patients/' is set in the project's root urls.py
via include('patients.urls'). The router adds '' (list/create) and '<pk>/'
(detail actions) relative to that prefix.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PatientViewSet

# Create router and register our ViewSet
# basename='patient': Used to generate URL names like 'patient-list', 'patient-detail'
router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

# router.urls contains all auto-generated URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
