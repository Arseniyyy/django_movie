from rest_framework.test import APITestCase
from rest_framework import status

from movies.models import Movie
from movies.tests.factories.factories import (create_movie_factory,
                                              create_user_factory,
                                              create_actor_factory,
                                              create_genre_factory,)


MODEL_URL = "/api/v1/movie/"
CREATE_ACTOR_URL = "/api/v1/actor/"


def create_sample_instance(**params):
    return Movie.objects.create(**params)


class MovieAPITest(APITestCase):
    """Tests the CRUD functions of the model. Also runs a string representation test."""

    def setUp(self) -> None:
        actor = create_actor_factory()
        genre = create_genre_factory()
        self.staff_user = create_user_factory(is_staff=True)
        self.movie_payload = {"title": "Slumberland",
                              "url": "new-url-1",
                              "description": "default",
                              "directors": [
                                  actor.pk
                              ],
                              "genres": [
                                  genre.pk
                              ],
                              "poster": "none"}
        self.client.force_authenticate(user=self.staff_user)

    def test_string_representation(self):
        # TODO: this piece of code is repeatable. Rewrite it in a different place, so it can be accessible by other functions
        user = create_user_factory(email='test@test-str-representation.com')
        movie = create_movie_factory(user)
        self.assertEqual(str(movie), f'{movie.title} - {movie.year}')

    def test_get_absolute_url(self):
        user = create_user_factory(
            email='test@test-get-absolute-url-representation.com')
        movie = create_movie_factory(user)
        response = self.client.get(
            movie.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_model(self):
        response = self.client.get(
            MODEL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_model(self):
        """Tests that a model gets created well."""
        response = self.client.post(MODEL_URL, self.movie_payload)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_retrieve_model(self):
        """Tests that a model gets retrieved well."""
        movie = create_movie_factory(user=self.staff_user)
        movie_detail_url = f'{MODEL_URL}{movie.pk}/'
        response = self.client.get(
            movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        movie = create_movie_factory(user=self.staff_user)
        movie_detail_url = f'{MODEL_URL}{movie.pk}/'
        payload = {"title": "New name of the movie"}
        response = self.client.patch(
            movie_detail_url, payload)
        instance = response.data
        self.assertEqual(instance.get("title"), payload.get("title"))

    def test_delete_model(self):
        movie = create_movie_factory(user=self.staff_user)
        movie_detail_url = f'{MODEL_URL}{movie.pk}/'
        response_delete = self.client.delete(
            movie_detail_url)
        response_get = self.client.get(
            movie_detail_url)
        self.assertEqual(response_delete.status_code,
                         status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)
