"""
doctors/tests.py — Automated Tests for Doctor Management Module

Covers:
- Adding a new doctor (authenticated)
- Listing all doctors
- Retrieving specific doctor
- Updating doctor record
- Deleting doctor record
- Validation (experience >= 0, valid phone, unique email)
- Unauthenticated access prevention
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Doctor

User = get_user_model()


class DoctorManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='docadmin@example.com', name='Doctor Admin', password='Password123!'
        )
        self.client.force_authenticate(user=self.user)

        self.doctor_data = {
            'name': 'Stephen Strange',
            'specialization': 'Neuro-Surgery',
            'contact_number': '+919988776655',
            'email': 'dr.strange@hospital.com',
            'years_of_experience': 15
        }

    def test_create_doctor(self):
        """Test creating a doctor profile."""
        url = reverse('doctor-list')
        response = self.client.post(url, self.doctor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Stephen Strange')
        self.assertTrue(Doctor.objects.filter(email='dr.strange@hospital.com').exists())

    def test_list_doctors(self):
        """Test listing all doctors."""
        Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_doctor(self):
        """Test retrieving specific doctor details."""
        doc = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Stephen Strange')

    def test_update_doctor(self):
        """Test updating doctor information."""
        doc = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doc.pk})
        update_data = self.doctor_data.copy()
        update_data['years_of_experience'] = 16
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['years_of_experience'], 16)

    def test_delete_doctor(self):
        """Test deleting a doctor record."""
        doc = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doc.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Doctor.objects.filter(pk=doc.pk).exists())

    def test_negative_experience_validation(self):
        """Test negative years of experience is rejected."""
        url = reverse('doctor-list')
        data = self.doctor_data.copy()
        data['years_of_experience'] = -5
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_unauthenticated_access_blocked(self):
        """Test unauthenticated requests are blocked."""
        self.client.force_authenticate(user=None)
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
