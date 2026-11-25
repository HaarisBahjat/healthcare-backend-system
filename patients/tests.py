"""
patients/tests.py — Automated Tests for Patient Management Module

Covers:
- Creating a patient (authenticated)
- Listing patients created by the authenticated user
- Data isolation (User A cannot see User B's patients)
- Retrieving, updating, and deleting patient records
- Unauthenticated access restrictions (401 Unauthorized)
- Validation rules (phone number format, required fields)
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Patient

User = get_user_model()


class PatientManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com', name='User One', password='Password123!'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com', name='User Two', password='Password123!'
        )

        # Authenticate as user1 by default
        self.client.force_authenticate(user=self.user1)

        self.patient_data = {
            'name': 'Bruce Banner',
            'date_of_birth': '1975-12-18',
            'gender': 'Male',
            'contact_number': '+919876543210',
            'medical_history': 'Gamma radiation exposure'
        }

    def test_create_patient(self):
        """Test creating a patient sets created_by to current user."""
        url = reverse('patient-list')
        response = self.client.post(url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Bruce Banner')
        self.assertEqual(response.data['data']['created_by'], 'user1@example.com')

    def test_user_data_isolation(self):
        """Test user1 only sees user1's patients, not user2's patients."""
        # Create patient for user1
        p1 = Patient.objects.create(created_by=self.user1, **self.patient_data)
        # Create patient for user2
        data2 = self.patient_data.copy()
        data2['name'] = 'Tony Stark'
        p2 = Patient.objects.create(created_by=self.user2, **data2)

        # Query as user1
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [p['name'] for p in response.data]
        self.assertIn('Bruce Banner', names)
        self.assertNotIn('Tony Stark', names)

        # Attempt to retrieve user2's patient directly -> should return 404
        detail_url = reverse('patient-detail', kwargs={'pk': p2.pk})
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_patient(self):
        """Test updating patient details."""
        p = Patient.objects.create(created_by=self.user1, **self.patient_data)
        url = reverse('patient-detail', kwargs={'pk': p.pk})
        update_data = self.patient_data.copy()
        update_data['name'] = 'Bruce Banner, PhD'
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Bruce Banner, PhD')

    def test_delete_patient(self):
        """Test deleting a patient."""
        p = Patient.objects.create(created_by=self.user1, **self.patient_data)
        url = reverse('patient-detail', kwargs={'pk': p.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Patient.objects.filter(pk=p.pk).exists())

    def test_unauthenticated_access_blocked(self):
        """Test that unauthenticated requests to patients endpoints return 401."""
        self.client.force_authenticate(user=None)
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_invalid_phone_number_validation(self):
        """Test invalid phone numbers are rejected."""
        url = reverse('patient-list')
        data = self.patient_data.copy()
        data['contact_number'] = '123'  # Too short
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
