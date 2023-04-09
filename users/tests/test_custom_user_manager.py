from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "12345"
        user_model = get_user_model()
        self.manager = user_model.objects

    def test_create_user_without_email(self):
        """Tests if a user's email is set to `None`."""
        with self.assertRaises(ValueError):
            self.manager.create_user(email=None, password=self.password)

    def test_superuser_is_staff(self):
        """Tests if user's attribute `is_staff` is set to `None`."""
        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email=self.email, password=self.password, is_staff=None)

    def test_superuser_is_superuser(self):
        """Tests if user's attribute `is_superuser` is set to `None`."""
        with self.assertRaises(ValueError):
            self.manager.create_superuser(email=self.email,
                                          password=self.password, is_superuser=None)
