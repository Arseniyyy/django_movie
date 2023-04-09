from socket import inet_aton

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.request import Request
from movies.models import Rating

from movies.tests.factories.factories import (create_user_factory,
                                              create_movie_factory,
                                              create_star_factory,)
from movies.views import ReviewListCreateAPIView, ListCreateRatingViewSet


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


class ListCreateRatingViewSetAPITest(APITestCase):
    def setUp(self) -> None:
        self.view = ListCreateRatingViewSet.as_view({"get": "list",
                                                     "post": "create"})
        self.url = "/api/v1/rating/"
        self.user = create_user_factory(is_staff=True)
        self.movie = create_movie_factory(user=self.user)
        self.star = create_star_factory()
        self.payload = {"star": self.star.pk,
                        "movie": self.movie.pk}
        self.wrong_payload = {"star": self.star.pk}  # movie key is absent
        self.factory = APIRequestFactory()

    def test_get_client_ip(self):
        request = self.factory.post(
            self.url, self.payload, HTTP_X_FORWARDED_FOR='127.0.0.1')
        force_authenticate(request=request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = self.factory.post(
            self.url, self.payload, REMOTE_ADDR='127.0.0.1')
        force_authenticate(request=request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rating(self):
        """Tests if `create` function can return the 400 http status code."""
        request = self.factory.post(self.url, self.wrong_payload)
        force_authenticate(request=request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
