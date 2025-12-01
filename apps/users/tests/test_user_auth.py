from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models.user_auth import User


class UserAuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('users:register')  # fixed namespace
        self.login_url = reverse('token_obtain_pair')  # SimpleJWT login endpoint
        self.user_data = {
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'email': 'testuser@example.com',
        }

        # Create user for login tests
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )

    def test_login_with_valid_credentials(self):
        """User can login and receive access and refresh tokens"""
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        """Login fails with wrong password"""
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_protected_endpoint_requires_auth(self):
        """Protected endpoints should require JWT access token"""
        protected_url = reverse('users:register_device')  # fixed namespace
        response = self.client.post(protected_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_token(self):
        """User can access protected endpoint using access token"""
        # Login first to get token
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        access_token = login_response.data['access']

        protected_url = reverse('users:register_device')  # fixed namespace
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(protected_url, {
            'device_model': 'iPhone 15',
            'operation_version': 'iOS 17',
            'device_type': 'IOS',
            'device_id': 'DEVICE123',
            'ip_address': '127.0.0.1',
            'app_version': '1.0.0',
            'firebase_token': 'FAKE_TOKEN',
            'language': 'EN',
            'theme': 'LIGHT'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('device_token', response.data)
