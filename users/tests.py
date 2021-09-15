from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users_app:auth_register')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'testuser@nextontext.com',
            'password': 'testpass',
            'username': 'nextontext',
            'first_name': 'Ilia',
            'last_name': 'Zaraysky'
        }
        res = self.client.post(CREATE_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payloads = {
            'email': 'testuser@nextontext.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payloads, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payloads['email']
        ).exists()
        self.assertFalse(user_exists)
