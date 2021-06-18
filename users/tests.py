from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
class LoginApiTest(TestCase):

    active_username = settings.TEST_USER
    active_password = settings.TEST_USER_PASSWORD
    inactive_username = 'jose.antonio@test.com'
    inactive_password = '123456'
    active_user_data = {
        'email': active_username,
        'first_name': 'Chuy',
        'is_superuser': True,
        'is_staff': True,
        'is_active': True,
        'last_name': 'Naranjo',
        'password': active_password
    }
    inactive_user_data = {
        'email': inactive_username,
        'first_name': 'José',
        'is_superuser': True,
        'is_staff': True,
        'is_active': False,
        'last_name': 'Antonio',
        'password': inactive_password
    }

    def setUp(self):
        User.objects.create_superuser(**self.active_user_data)
        User.objects.create_superuser(**self.inactive_user_data)

    def test_login_without_data(self):
        print('Login_without_data.')
        client = APIClient()
        client.default_format='json'
        res = client.post('/api/login/', {})
        self.assertIn('email', res.data.keys())
        self.assertIn('password', res.data.keys())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_data_blank(self):
        print('Login with data in blank.')
        client = APIClient()
        client.default_format='json'
        payload = {'email': '','password': ''}
        res = client.post('/api/login/', payload)
        self.assertIn('email', res.data.keys())
        self.assertIn('password', res.data.keys())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        print('Invalid email.')
        client = APIClient()
        client.default_format='json'
        payload = {'email': 'test', 'password': '123456'}
        res = client.post('/api/login/', payload)
        self.assertIn('email', res.data.keys())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unregistered_use(self):
        print('Unregistered user.')
        client = APIClient()
        client.default_format='json'
        payload = {'email': 'test@test.com','password': '123456'}
        res = client.post('/api/login/', payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_with_inactive_user(self):
        print('Login with inactive user.')
        client = APIClient()
        client.default_format='json'
        payload = {
            'email': self.inactive_username,
            'password': self.inactive_password,
        }
        res = client.post('/api/login/', payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_incorrect_password(self):
        print('Incorrect password.')
        client = APIClient()
        client.default_format='json'
        payload = {
            'email': self.active_username,
            'password': 'test',
        }
        res = client.post('/api/login/', payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_successfully(self):
        print('Login successfully.')
        client = APIClient()
        client.default_format='json'
        payload = {
            'email': self.active_username,
            'password': self.active_password,
        }
        res = client.post('/api/login/', payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
