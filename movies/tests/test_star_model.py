from rest_framework.test import APITestCase

from movies.tests.factories.factories import (create_star_factory,)


class StarAPITest(APITestCase):
    def setUp(self):
        self.star = create_star_factory()

    def test_str_method(self):
        self.assertEqual(str(self.star), str(self.star.value))
