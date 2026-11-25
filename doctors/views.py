"""
doctors/views.py — Doctor API Views

Implements full CRUD operations for doctors:
- POST   /api/doctors/       → Add a new doctor (Authenticated users only)
- GET    /api/doctors/       → Retrieve all doctors
- GET    /api/doctors/<id>/  → Get details of a specific doctor
- PUT    /api/doctors/<id>/  → Update doctor details
- DELETE /api/doctors/<id>/  → Delete a doctor record
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctor entity CRUD management.

    Enforces JWT authentication across all endpoints as specified in requirements.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        Create a new doctor with structured response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Doctor created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update doctor record with structured response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Doctor updated successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a doctor record with structured response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Doctor deleted successfully.'
        }, status=status.HTTP_200_OK)
