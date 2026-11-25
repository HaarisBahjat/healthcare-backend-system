"""
doctors/models.py — Doctor Data Model

Defines the Doctor entity stored in the database.

Fields:
- name: Full name of the doctor.
- specialization: Field of medical practice (Cardiology, Dermatology, etc.).
- contact_number: Direct phone contact for the doctor.
- email: Doctor's professional contact email (unique).
- years_of_experience: Number of years practicing medicine (positive integer).
- created_at / updated_at: System timestamps.
"""

from django.db import models


class Doctor(models.Model):
    """
    Represents a Doctor entity in the healthcare system.

    Attributes:
        name (str): Full name of the medical practitioner.
        specialization (str): Area of expertise / department.
        contact_number (str): Contact phone number.
        email (str): Unique business email.
        years_of_experience (int): Years of clinical experience.
        created_at (datetime): Automatically set timestamp upon creation.
        updated_at (datetime): Automatically updated timestamp.
    """

    name = models.CharField(
        max_length=255,
        help_text='Full name of the doctor'
    )

    specialization = models.CharField(
        max_length=255,
        help_text='Medical specialization (e.g., Cardiology, Neurology, Pediatrics)'
    )

    contact_number = models.CharField(
        max_length=15,
        help_text='Doctor phone number (e.g. +919876543210)'
    )

    email = models.EmailField(
        unique=True,
        max_length=255,
        help_text='Unique professional email address for the doctor'
    )

    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text='Number of years in medical practice'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the doctor record was added'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when the doctor record was last updated'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
