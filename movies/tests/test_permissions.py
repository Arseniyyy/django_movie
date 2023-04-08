from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from movies.models import Review

from users.models import CustomUser
from movies.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from movies.tests.factories.factories import create_user_factory, create_movie_factory, create_review_factory


class IsAdminOrReadOnlyTestCase(APITestCase):
    def setUp(self):
        staf_email = "staff@example.com"
        user_email = "user@example.com"
        password = "password"
        self.actor_payload = {"name": "Romeo",
                              "age": 20,
                              "description": "desc"}
        self.staff_user = CustomUser.objects.create_user(email=staf_email,
                                                         password=password,
                                                         is_staff=True)
        self.non_staff_user = CustomUser.objects.create_user(email=user_email,
                                                             password=password)
        self.url = "/api/v1/actor/"

    def test_get_request_for_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_for_non_staff_user(self):
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_request_for_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, self.actor_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_request_for_non_staff_user(self):
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IsOwnerOrReadOnlyTestCase(APITestCase):
    def setUp(self) -> None:
        owner_email = "user@example.com"
        non_owner_email = "anyone@example.com"
        password = "password"

        self.non_owner = create_user_factory(
            email=non_owner_email, password=password)
        self.owner = create_user_factory(email=owner_email, password=password)
        movie = create_movie_factory(user=self.owner)
        review = create_review_factory(movie, user=self.owner)
        self.url = f'/api/v1/review/{review.pk}/'

    def test_get_request_for_not_owner(self):
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_request_for_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_request_for_not_owner(self):
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
