from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_movie_factory,
                                              create_user_factory,
                                              create_rating_factory,
                                              create_star_factory,)


class RatingAPITestCase(APITestCase):
    def setUp(self) -> None:
        user = create_user_factory()
        self.movie = create_movie_factory(user=user)
        self.star = create_star_factory()
        self.rating = create_rating_factory(movie=self.movie, star=self.star)

    def test_str_method(self):
        self.assertEqual(str(self.rating), f'{self.star} - {self.movie}')
