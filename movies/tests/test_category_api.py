from rest_framework.test import APITestCase

from movies.tests.factories.factories import create_category_factory


class CategoryTestAPI(APITestCase):
    def test_string_representation(self):
        category = create_category_factory()
        self.assertEqual(str(category), category.name)
