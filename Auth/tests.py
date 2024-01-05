import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('create_user')
        self.login_url = reverse('sign_in')
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        self.login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        self.invalid_login_data = {
            'email': 'testuser@example.com',
            'password': 'wrong',
        }

    def test_create_user(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, 'testuser@example.com')

    def test_create_user_invalid_data(self):
        response = self.client.post(self.signup_url, data={})
        self.assertEqual(response.status_code, 400)

    def test_sign_in(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, data=self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)

    def test_sign_in_invalid_credentials(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, data=self.invalid_login_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_sign_in_invalid_data(self):
        response = self.client.post(self.login_url, data={})
        self.assertEqual(response.status_code, 400)
