from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser
from movies.tests.factories.factories import create_user_factory, create_movie_factory, create_review_factory


class IsAdminOrReadOnlyTestCase(APITestCase):
    def setUp(self):
        non_staff_email = "test@example1.com"
        self.actor_payload = {"name": "Romeo",
                              "age": 20,
                              "description": "desc"}
        self.staff_user = create_user_factory(is_staff=True)
        self.non_staff_user = create_user_factory(email=non_staff_email)
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
        self.non_owner = create_user_factory(
            email=non_owner_email)
        self.owner = create_user_factory(email=owner_email)
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
