"""
accounts/tests.py — Automated Tests for Authentication Module

Covers:
- Successful user registration
- Duplicate email registration prevention
- Missing/invalid registration fields
- User login returning access & refresh JWT tokens
- Login with invalid credentials
- Token refresh endpoint
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('token-refresh')
        self.user_data = {
            'name': 'Test User',
            'email': 'authtest@example.com',
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }

    def test_user_registration_success(self):
        """Test registering a new user with valid details."""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['email'], 'authtest@example.com')
        self.assertTrue(User.objects.filter(email='authtest@example.com').exists())

    def test_user_registration_without_password2(self):
        """Test registering with only name, email, and password."""
        data = {
            'name': 'Direct Reg User',
            'email': 'directreg@example.com',
            'password': 'SecurePassword123!'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['email'], 'directreg@example.com')

    def test_user_registration_duplicate_email(self):
        """Test that registering with an existing email returns 400 Bad Request."""
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_user_registration_password_mismatch(self):
        """Test that mismatched passwords fail validation."""
        data = self.user_data.copy()
        data['password2'] = 'Mismatch123!'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test login returns JWT access and refresh tokens."""
        self.client.post(self.register_url, self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    def test_user_login_invalid_credentials(self):
        """Test login with wrong password returns 401 Unauthorized."""
        self.client.post(self.register_url, self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_token_refresh(self):
        """Test refreshing an access token using a refresh token."""
        self.client.post(self.register_url, self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['refresh']

        refresh_response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
