"""
mappings/views.py — Patient-Doctor Mapping API Views

APIs implemented:
1. POST   /api/mappings/              - Assign a doctor to a patient
2. GET    /api/mappings/              - Retrieve all patient-doctor mappings
3. GET    /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient
4. DELETE /api/mappings/<id>/         - Remove a doctor from a patient (delete mapping)
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingListCreateView(APIView):
    """
    Handles:
    - POST /api/mappings/ -> Assign doctor to patient
    - GET  /api/mappings/ -> Retrieve all mappings
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieve all mappings.
        """
        mappings = PatientDoctorMapping.objects.select_related('patient', 'doctor').all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Assign a doctor to a patient.
        """
        serializer = PatientDoctorMappingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()
        return Response({
            'success': True,
            'message': 'Doctor assigned to patient successfully.',
            'data': PatientDoctorMappingSerializer(mapping, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class PatientDoctorsDetailView(APIView):
    """
    Handles:
    - GET /api/mappings/<patient_id>/ -> Get all doctors assigned to a specific patient
    - DELETE /api/mappings/<id>/       -> Remove a mapping by its primary key ID
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """
        Retrieve all doctors assigned to a specific patient.
        pk is interpreted as patient_id.
        """
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related('doctor')
        doctors = [m.doctor for m in mappings]
        doctor_serializer = DoctorSerializer(doctors, many=True)

        return Response({
            'patient_id': patient.id,
            'patient_name': patient.name,
            'assigned_doctors_count': len(doctors),
            'doctors': doctor_serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Remove a doctor from a patient by mapping ID.
        Ensures the user owns the associated patient.
        """
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk, patient__created_by=request.user)
        mapping.delete()
        return Response({
            'success': True,
            'message': 'Doctor removed from patient successfully.'
        }, status=status.HTTP_200_OK)
