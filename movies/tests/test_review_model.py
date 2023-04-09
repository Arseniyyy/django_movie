from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_movieshot_factory,
                                              create_movie_factory,
                                              create_user_factory,
                                              create_rating_factory,
                                              create_star_factory,
                                              create_review_factory)


class ReviewAPITest(APITestCase):
    def setUp(self):
        user = create_user_factory()
        self.movie = create_movie_factory(user=user)
        self.review = create_review_factory(movie=self.movie, user=user)

    def test_str_method(self):
        self.assertEqual(str(self.review),
                         f'{self.review.name} - {self.review.movie}')
