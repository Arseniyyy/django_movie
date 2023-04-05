from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from movies.models import Movie, Actor
from movies.tests.factories.factories import (create_movie_factory,
                                              create_user_factory,
                                              create_category_factory,
                                              create_reviews_set)
from users.models import CustomUser
from users.tests.test_user_api import CREATE_USER_URL, TOKEN_URL


MODEL_URL = "/api/v1/movie/"
CREATE_ACTOR_URL = "/api/v1/actor/"


def create_sample_instance(**params):
    return Movie.objects.create(**params)


class MovieAPITest(APITestCase):
    """Tests the CRUD functions of the model. Also runs a string representation test."""

    def setUp(self) -> None:
        self.email = "test@test.com"
        self.password = "WhoSellsWind205"

        user_payload = {"email": "test@test.com",
                        "password": "WhoSellsWind205"}
        actor_payload = {"name": "Romeo",
                         "age": 20,
                         "description": "desc"}
        self.user_response = self.client.post(CREATE_USER_URL, {"email": user_payload.get('email'),
                                                                "password": user_payload.get('password'),
                                                                "re_password": user_payload.get('password')})
        self.access_token_response = self.client.post(TOKEN_URL, {"email": user_payload.get('email'),
                                                                  "password": user_payload.get('password')})
        self.auth_header = f'Bearer {self.access_token_response.data.get("access")}'
        self.actor_response = self.client.post(
            CREATE_ACTOR_URL, actor_payload, HTTP_AUTHORIZATION=self.auth_header)

        self.movie_payload = {
            "title": "Slumberland",
            "url": "new-url-1",
            "directors": [
                self.actor_response.data.get("id")
            ],
            "poster": "none"
        }
        self.movie_response = self.client.post(
            MODEL_URL, self.movie_payload, HTTP_AUTHORIZATION=self.auth_header)
        self.movie_detail_url = f'{MODEL_URL}{self.movie_response.data.get("id")}/'

    def test_string_representation(self):
        # TODO: this piece of code is repeatable. Rewrite it in a different place, so it can be accessible by other functions
        user = create_user_factory()
        category = create_category_factory()
        movie = create_movie_factory(user, category)
        self.assertEqual(str(movie), f'{movie.title} - {movie.year}')

    def test_get_absolute_url(self):
        user = create_user_factory()
        category = create_category_factory()
        movie = create_movie_factory(user, category)
        response = self.client.get(
            movie.get_absolute_url(), HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)

    def test_create_model(self):
        """Tests that a model gets created well."""
        self.assertEqual(self.movie_response.status_code,
                         status.HTTP_201_CREATED)

    def test_retrieve_model(self):
        """Tests that a model gets retrieved well."""
        response = self.client.get(
            self.movie_detail_url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        payload = {"title": "New name of the movie"}
        response = self.client.patch(
            self.movie_detail_url, payload, HTTP_AUTHORIZATION=self.auth_header)
        instance = response.data
        self.assertEqual(instance.get("title"), payload.get("title"))

    def test_delete_model(self):
        response_delete = self.client.delete(
            self.movie_detail_url, HTTP_AUTHORIZATION=self.auth_header)
        response_get = self.client.get(
            self.movie_detail_url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response_delete.status_code,
                         status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)
