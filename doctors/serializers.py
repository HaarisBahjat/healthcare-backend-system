"""
doctors/serializers.py — Doctor Serializers

Transforms Doctor model instances to and from JSON format, ensuring
field validation and proper data formatting.
"""

import re
from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Doctor model.

    Validates:
    - Unique email per doctor
    - Non-negative years of experience
    - Contact number regex
    - Non-empty name and specialization
    """

    class Meta:
        model = Doctor
        fields = (
            'id',
            'name',
            'specialization',
            'contact_number',
            'email',
            'years_of_experience',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_contact_number(self, value):
        """
        Validate contact number format (supports E.164 and common 7-15 digit phone formats).
        """
        phone_pattern = r'^\+?[0-9]{7,15}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError(
                'Enter a valid contact number (7 to 15 digits, optionally prefixed with +).'
            )
        return value

    def validate_years_of_experience(self, value):
        """
        Validate that years of experience is a non-negative number.
        """
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Doctor name cannot be blank.')
        return value.strip()
