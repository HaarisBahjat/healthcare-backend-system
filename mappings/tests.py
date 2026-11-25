"""
mappings/tests.py — Automated Tests for Patient-Doctor Mapping Module

Covers:
- Assigning a doctor to a patient
- Listing all mappings
- Retrieving all doctors assigned to a specific patient
- Preventing duplicate mapping assignments (unique_together)
- Data isolation (cannot assign doctor to another user's patient)
- Removing a doctor from a patient
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from patients.models import Patient
from doctors.models import Doctor
from .models import PatientDoctorMapping

User = get_user_model()


class PatientDoctorMappingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='mappinguser@example.com', name='Mapping User', password='Password123!'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com', name='Other User', password='Password123!'
        )
        self.client.force_authenticate(user=self.user)

        self.patient = Patient.objects.create(
            created_by=self.user,
            name='Peter Parker',
            date_of_birth='2001-08-10',
            gender='Male',
            contact_number='+919876543210'
        )
        self.doctor = Doctor.objects.create(
            name='Dr. Curt Connors',
            specialization='Genetics',
            contact_number='+919123456780',
            email='dr.connors@science.edu',
            years_of_experience=20
        )

    def test_assign_doctor_to_patient(self):
        """Test assigning a doctor to a patient."""
        url = reverse('mapping-list-create')
        data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['patient']['id'], self.patient.id)
        self.assertEqual(response.data['data']['doctor']['id'], self.doctor.id)

    def test_prevent_duplicate_mapping(self):
        """Test assigning the same doctor to the same patient twice is rejected."""
        url = reverse('mapping-list-create')
        data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id
        }
        # First assignment
        self.client.post(url, data)
        # Duplicate assignment
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_user_cannot_map_other_users_patient(self):
        """Test a user cannot assign doctors to a patient they did not create."""
        other_patient = Patient.objects.create(
            created_by=self.other_user,
            name='Miles Morales',
            date_of_birth='2005-01-01',
            gender='Male',
            contact_number='+919876543299'
        )
        url = reverse('mapping-list-create')
        data = {
            'patient_id': other_patient.id,
            'doctor_id': self.doctor.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('patient_id', response.data['errors'])

    def test_get_doctors_assigned_to_patient(self):
        """Test retrieving all doctors for a specific patient."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        url = reverse('mapping-detail', kwargs={'pk': self.patient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assigned_doctors_count'], 1)
        self.assertEqual(response.data['doctors'][0]['name'], 'Dr. Curt Connors')

    def test_remove_doctor_from_patient(self):
        """Test removing a doctor mapping."""
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        url = reverse('mapping-detail', kwargs={'pk': mapping.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(PatientDoctorMapping.objects.filter(pk=mapping.id).exists())
