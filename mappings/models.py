"""
mappings/models.py — Patient-Doctor Mapping Data Model

Represents the relationship/assignment between a Patient and a Doctor.

Key Architectural Decisions:
1. ForeignKeys:
   - patient: Points to Patient model (CASCADE on delete).
   - doctor: Points to Doctor model (CASCADE on delete).
2. Constraints:
   - UniqueConstraint on ('patient', 'doctor') prevents assigning the same doctor
     to the same patient more than once (avoids duplicates at the DB level).
3. Metadata:
   - assigned_at: Records timestamp of assignment.
"""

from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Mapping model linking a Patient with an assigned Doctor.
    """

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings',
        help_text='The patient being assigned a doctor'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings',
        help_text='The doctor assigned to the patient'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the doctor was assigned to the patient'
    )

    class Meta:
        ordering = ['-assigned_at']
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        # Prevent assigning the same doctor to the same patient multiple times
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"Patient: {self.patient.name} <-> Dr. {self.doctor.name}"
