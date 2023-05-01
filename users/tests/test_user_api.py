from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from movies.tests.factories.factories import create_user_factory


class UserAPITest(APITestCase):
    def setUp(self):
        self.create_user_url = '/auth/users/'
        self.obtain_refresh_token_url = '/auth/jwt/token/refresh/'
        self.obtain_jwt_token_pair = '/auth/jwt/token/'
        self.payload = {
            "email": "test@test.com",
            "password": "WhoSellsWind205",
            "re_password": "WhoSellsWind205"
        }
        self.payload_without_re_password = {
            "email": "test@test.com",
            "password": "WhoSellsWind205"
        }
        self.wrong_payload = {
            'email': 'test@test.com',
            'password': 'ha',
            're_password2': 'ha'
        }
        self.payload_without_password = {
            "email": "test@test.com",
            "password": ""
        }

    def create_user(self, **params):
        return get_user_model().objects.create_user(**params)

    def test_str_representation(self):
        user = create_user_factory()
        self.assertEqual(str(user), user.email)

    def test_create_user(self):
        "Tests if a user model gets created well with a payload."
        res = self.client.post(self.create_user_url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        """Tests creating user that already exists"""
        self.create_user(**self.payload_without_re_password)

        res = self.client.post(self.create_user_url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Tests that password must be more than 5 characters"""
        res = self.client.post(self.create_user_url, self.wrong_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # check if a user instance wasn't created with the wrong payload
        user_exists = get_user_model().objects.filter(
            email=self.wrong_payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_jwt_token_for_user(self):
        """Tests that a jwt token gets created well."""
        self.create_user(**self.payload_without_re_password)
        res = self.client.post(self.obtain_jwt_token_pair, {'email': self.payload['email'],
                                           'password': self.payload['password'],
                                           're_password': self.payload['re_password']})
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_jwt_token_for_user(self):
        """Tests that a refresh token gets created well."""
        self.client.post(self.create_user_url, self.payload)

        from users.tests.activation_email import EMAILS
        uid = EMAILS.get('test@test.com').get('uid')
        token = EMAILS.get('test@test.com').get('token')
        self.client.post('/auth/users/activation/', {
            'uid': uid,
            'token': token
        })
        response = self.client.post(self.obtain_jwt_token_pair, {
            'email': self.payload.get('email'),
            'password': self.payload.get('password')
        })
        res = self.client.post(self.obtain_refresh_token_url, {
                                'refresh': response.data['refresh']})

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Tests that a token is not created when invalid credentials are given."""
        self.create_user(**self.payload_without_re_password)
        payload2 = {
            'email': 'test@test.com',
            'password': 'wrong'
        }
        res = self.client.post(self.obtain_jwt_token_pair, payload2)

        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        """Tests if email and password are required."""
        res = self.client.post(self.obtain_jwt_token_pair, self.payload_without_password)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
