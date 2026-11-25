"""
patients/models.py — Patient Data Model

Defines the Patient entity stored in the database.

Key design decisions:
- Each patient is linked to the user who created them via 'created_by' (ForeignKey).
  This enables data isolation: users can only see/manage their own patients.
- on_delete=CASCADE: If a user account is deleted, their patient records are also
  removed. This maintains referential integrity in the database.
- related_name='patients': Allows reverse lookup from User, e.g. user.patients.all()
"""

from django.conf import settings
from django.db import models


class Patient(models.Model):
    """
    Represents a patient record in the healthcare system.

    Fields:
        created_by: The authenticated user who created this patient record.
                    Used for access control — users only see their own patients.
        name: Full name of the patient.
        date_of_birth: Patient's date of birth, used for age calculation.
        gender: Patient's gender (Male, Female, Other) — uses choices for validation.
        contact_number: Phone number for reaching the patient (max 15 chars for intl formats).
        medical_history: Free-text field for recording past diagnoses, allergies, etc.
        created_at: Auto-set timestamp when the record is first created.
        updated_at: Auto-updated timestamp whenever the record is modified.
    """

    # Gender choices — using a tuple of tuples for Django's 'choices' parameter.
    # Why choices? Restricts input to valid options at both the database and
    # serializer level, preventing invalid data like "xyz" from being stored.
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    # ForeignKey to the User model — links each patient to its creator.
    # settings.AUTH_USER_MODEL: References our CustomUser model dynamically.
    # Why not import CustomUser directly? Using settings.AUTH_USER_MODEL is the
    # Django best practice — it avoids circular imports and works even if the
    # user model is swapped later.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients',
        help_text='The user who created this patient record'
    )

    name = models.CharField(
        max_length=255,
        help_text='Full name of the patient'
    )

    date_of_birth = models.DateField(
        help_text='Date of birth (YYYY-MM-DD format)'
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        help_text='Gender of the patient (Male, Female, or Other)'
    )

    contact_number = models.CharField(
        max_length=15,
        help_text='Phone number (supports international format, e.g. +919876543210)'
    )

    medical_history = models.TextField(
        blank=True,
        default='',
        help_text='Optional free-text field for past diagnoses, allergies, conditions, etc.'
    )

    # auto_now_add=True: Set once when the object is first created, never changes.
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when this record was created'
    )

    # auto_now=True: Updated every time .save() is called on this object.
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp of the last update to this record'
    )

    class Meta:
        # Default ordering: most recently created patients appear first
        ordering = ['-created_at']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"{self.name} (DOB: {self.date_of_birth})"
