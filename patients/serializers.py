"""
patients/serializers.py — Patient Serializer

Handles validation and transformation of Patient data between
JSON (API layer) and Python objects (Django ORM layer).

Key points:
- 'created_by' is read-only — it's auto-set from the authenticated user
  in the view's perform_create(), never from user input.
- All date and choice fields are validated automatically by DRF based
  on the model field definitions (DateField, choices, max_length, etc.).
"""

import re
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model with strict validation.
    """

    # Display the creator's email instead of just the user ID.
    created_by = serializers.CharField(
        source='created_by.email',
        read_only=True
    )

    class Meta:
        model = Patient
        fields = (
            'id',
            'created_by',
            'name',
            'date_of_birth',
            'gender',
            'contact_number',
            'medical_history',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_contact_number(self, value):
        """
        Validate contact number format (supports E.164 and common 10-15 digit phone formats).
        """
        phone_pattern = r'^\+?[0-9]{7,15}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError(
                'Enter a valid contact number (7 to 15 digits, optionally prefixed with +).'
            )
        return value

    def validate_name(self, value):
        """
        Ensure name is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError('Patient name cannot be blank.')
        return value.strip()
