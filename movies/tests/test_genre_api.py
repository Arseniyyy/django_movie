from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_genre_factory)


class GenreTestAPI(APITestCase):
    def setUp(self) -> None:
        self.genre = create_genre_factory()

    def test_str_method(self):
        self.assertEqual(str(self.genre), self.genre.name)
