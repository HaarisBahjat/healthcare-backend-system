"""
mappings/urls.py — Patient-Doctor Mapping URL Routes

Matches:
- /api/mappings/      -> POST (Assign doctor), GET (List all mappings)
- /api/mappings/<pk>/ -> GET (List doctors for patient_id), DELETE (Remove mapping by ID)
"""

from django.urls import path
from .views import PatientDoctorMappingListCreateView, PatientDoctorsDetailView

urlpatterns = [
    path('', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', PatientDoctorsDetailView.as_view(), name='mapping-detail'),
]
