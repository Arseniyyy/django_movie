from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_movieshot_factory,
                                              create_movie_factory,
                                              create_user_factory)


class MovieShotAPITest(APITestCase):
    def setUp(self):
        user = create_user_factory()
        movie = create_movie_factory(user=user)
        self.movieshot = create_movieshot_factory(movie=movie)

    def test_str_method(self):
        self.assertEqual(str(self.movieshot), self.movieshot.title)
