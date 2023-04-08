from rest_framework.test import APITestCase
from rest_framework import status

from movies.tests.factories.factories import (create_user_factory,)
from movies.views import ReviewListCreateAPIView


class ReviewListCreateAPIViewAPITest(APITestCase):
    """An `APITestCase` class for `ReviewListCreateAPIView`"""

    def setUp(self):
        self.url = "/api/v1/review/"
        user = create_user_factory(is_staff=True)
        self.client.force_authenticate(user=user)

    def test_get_serializer_class(self):
        """Tests if the right serializer is returned."""
        # test get request
        view = ReviewListCreateAPIView()
        response_get = self.client.get(self.url)
        view.request = response_get
        view.request.method = "GET"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, view.list_serializer_class)

        # test post request
        response_post = self.client.post(self.url)
        view.request = response_post
        view.request.method = "POST"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, view.create_serializer_class)

        # test another method for a request, for example, patch
        response_update = self.client.patch(self.url)
        view.request = response_update
        view.request.method = "PATCH"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, view.create_serializer_class)
