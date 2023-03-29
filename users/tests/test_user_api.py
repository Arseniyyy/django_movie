from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = '/auth/users/'
TOKEN_URL = '/auth/jwt/token/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "email": "test@test.com",
            "password": "WhoSellsWind205",
            "re_password": "WhoSellsWind205"
        }

    def test_movie_str(self):
        "Tests if a user model gets created well with a payload."
        # payload = {
        #     "email": "test@test.com",
        #     "password": "WhoSellsWind205",
        #     "re_password": "WhoSellsWind205"
        # }
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        """Tests creating user that already exists"""
        payload1 = {
            'email': 'test@test.com',
            'password': 'hardtocrack',
            # "re_password": "hardtocrack"
        }
        # payload2 = {
        #     'email': 'test@test.com',
        #     'password': 'hardtocrack',
        #     're_password': 'hardtocrack'
        # }
        create_user(**payload1)

        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Tests that password must be more than 5 characters"""
        wrong_payload = {
            'email': 'test@test.com',
            'password': 'ha',
            're_password2': 'ha'
        }
        res = self.client.post(CREATE_USER_URL, wrong_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # check if the user doesn't exist
        user_exists = get_user_model().objects.filter(
            email=wrong_payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_jwt_token_for_user(self):
        """Tests that a jwt token gets created well."""
        payload = {
            'email': 'test@test.com',
            'password': 'hardtocrack',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, {'email': payload['email'],
                                           'password': payload['password'],
                                           're_password': payload['password']})
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_jwt_token_for_user(self):
        """Tests that a refresh token gets created well."""
        pass
