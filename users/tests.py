# users/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthenticationTests(APITestCase):
    def setUp(self):
        # Define endpoint URLs using reverse for maintainability
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

    def test_user_registration_success(self):
        """
        Test that a user can successfully register.
        """
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ensure the user was created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_registration_password_mismatch(self):
        """
        Test that registration fails if passwords do not match.
        """
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPass123",
            "password2": "DifferentPass456"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for error message regarding password mismatch.
        self.assertIn('non_field_errors', response.data)

    def test_user_registration_missing_field(self):
        """
        Test that registration fails when a required field is missing.
        """
        payload = {
            "username": "testuser",
            # Email is missing intentionally.
            "password": "StrongPass123",
            "password2": "StrongPass123"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_success(self):
        """
        Test that a user can log in with valid credentials and receives JWT tokens.
        """
        # Create user directly in the database.
        User.objects.create_user(username="testuser", email="testuser@example.com", password="StrongPass123")
        
        login_payload = {
            "username": "testuser",
            "password": "StrongPass123"
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that tokens are returned.
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """
        Test that login fails with invalid credentials.
        """
        User.objects.create_user(username="testuser", email="testuser@example.com", password="StrongPass123")
        
        login_payload = {
            "username": "testuser",
            "password": "WrongPassword"
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)