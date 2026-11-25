"""
doctors/urls.py — Doctor Management URL Routes

Routes requests from /api/doctors/ to DoctorViewSet actions using DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

router = DefaultRouter()
router.register(r'', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('', include(router.urls)),
]
