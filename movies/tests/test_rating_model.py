from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_movie_factory,
                                              create_user_factory,
                                              create_rating_factory,)


class RatingAPITestCase(APITestCase):
    def setUp(self):
        user = create_user_factory()
        self.movie = create_movie_factory(user=user)
        self.rating = create_rating_factory(movie=self.movie)

    def test_str_method(self):
        self.assertEqual(str(self.rating), f'{self.rating.total_rating} - {self.movie}')
