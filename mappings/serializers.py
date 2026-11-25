"""
mappings/serializers.py — Serializers for Patient-Doctor Mapping

Provides representations for:
1. Creating a mapping (taking patient and doctor IDs with validation).
2. Detailed listing (including nested details of patient and doctor).
"""

from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and displaying Patient-Doctor Mappings.
    """

    # Accept IDs for write operations
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )

    # Read-only nested representations for clear API responses
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient_id',
            'doctor_id',
            'patient',
            'doctor',
            'assigned_at',
        )
        read_only_fields = ('id', 'patient', 'doctor', 'assigned_at')

    def validate(self, attrs):
        """
        Custom validation:
        1. Check if mapping already exists to give friendly error message.
        2. Ensure the requesting user owns the patient they are assigning a doctor to.
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        request = self.context.get('request')

        # Check user isolation: Patient must belong to the authenticated user
        if request and hasattr(request, 'user'):
            if patient.created_by != request.user:
                raise serializers.ValidationError({
                    'patient_id': 'You can only assign doctors to patients you created.'
                })

        # Check duplicate assignment
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError({
                'non_field_errors': ['This doctor is already assigned to this patient.']
            })

        return attrs
