"""
accounts/serializers.py — Serializers for Authentication

Serializers handle two jobs:
1. Validation: Ensure incoming data meets our rules (e.g., email format, password strength).
2. Transformation: Convert between Python objects and JSON for API input/output.

We define two serializers here:
- RegisterSerializer: Validates and creates new user accounts.
- LoginSerializer: Customizes the JWT token response to include user metadata.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# get_user_model() dynamically fetches whatever model is set in AUTH_USER_MODEL.
# Why: Avoids hardcoding 'accounts.CustomUser' — if the model name ever changes,
# this still works without updating every import.
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts: name, email, password, password2 (confirmation).
    Returns: id, name, email on success.

    Why ModelSerializer?
    - Automatically generates fields from the User model.
    - Provides built-in create/update logic that we customize below.
    """

    # password: write_only=True ensures it's accepted in input but NEVER
    # returned in API responses (security best practice for sensitive fields).
    # validate_password runs Django's built-in password validators
    # (min length, common passwords, numeric-only, etc.)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='Must be at least 8 characters, not entirely numeric, and not too common.'
    )

    # password2: Confirmation field — optional, but if provided, must match password.
    # Not a model field, so we declare it explicitly.
    password2 = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text='Optional confirmation password. If provided, must match password.'
    )

    class Meta:
        model = User
        # Fields exposed by this serializer:
        # - 'id' and 'email' are read from the model after creation
        # - 'name', 'password', 'password2' are accepted as input
        fields = ('id', 'name', 'email', 'password', 'password2')
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """
        Object-level validation — runs after individual field validators.

        Why validate() instead of validate_<field>()?
        - If password2 is supplied, compare it to password.
        """
        if 'password2' in attrs and attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Password fields do not match.'
            })
        return attrs

    def validate_email(self, value):
        """
        Field-level validation for email.

        Checks if a user with this email already exists.
        Why here instead of relying on the model's unique constraint?
        - Provides a cleaner, user-friendly error message instead of
          a raw database IntegrityError.
        """
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                'A user with this email address already exists.'
            )
        return value.lower()  # Normalize email to lowercase

    def create(self, validated_data):
        """
        Create and return a new user instance.

        Why override create()?
        - Remove 'password2' if present (not a model field).
        - Use create_user() to ensure password is properly hashed.
        """
        validated_data.pop('password2', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for returning user profile data.

    Used in login responses and anywhere we need to serialize
    user information without exposing sensitive fields like password.
    """

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at')
        read_only_fields = fields  # All fields are read-only
