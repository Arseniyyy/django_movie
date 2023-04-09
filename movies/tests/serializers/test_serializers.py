import os
import base64

from rest_framework.test import APITestCase, APIRequestFactory
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from dotenv import load_dotenv

from movies.serializers import Base64ImageField, RecursiveSerializer, ReviewSerializer
from movies.tests.serializers.image_data import image_data, invalid_image_data
from movies.tests.factories.factories import (create_user_factory,
                                              create_reviews_set,
                                              create_movie_factory,
                                              create_review_factory)


load_dotenv()


class Base64ImageFieldAPITest(APITestCase):
    """Tests that the serializer converts a base64 string to an image."""

    def setUp(self) -> None:
        self.serializer = Base64ImageField(max_length=None, use_url=True)

    def test_valid_data_with_headers(self):
        """
        Tests that a base64 string has `data:image/<extension>` header and the encoded data.
        In the case of the following code, the png extension is used.
        """
        validated_image_data = self.serializer.run_validation(
            image_data).read()
        encoded_validated_image_data = base64.b64encode(validated_image_data)
        decoded_validated_image_data = encoded_validated_image_data.decode()
        header, encoded_data = image_data.split(';base64,')
        expected_png_header = 'data:image/png'
        self.assertEqual(header, expected_png_header)
        self.assertEqual(encoded_data, decoded_validated_image_data)

    def test_invalid_data(self):
        """Tests if the passed data is invalid."""
        with self.assertRaises(ValidationError):
            self.serializer.run_validation(invalid_image_data)

    def test_image_to_base64_conversion(self):
        path_to_image = os.getenv('PATH_TO_IMAGE')
        with open(path_to_image, 'rb') as img:
            image_data = img.read()

        encoded_image_data = base64.b64encode(image_data)
        encoded_image_data = encoded_image_data.decode('utf-8')
        validated_image_data = self.serializer.run_validation(
            encoded_image_data)
        self.assertIsInstance(validated_image_data, ContentFile)


# class RecursiveSerializerAPITest(APITestCase):
#     def setUp(self) -> None:
#         # RecursiveSerializer can be tested using the review model.
#         self.url = '/api/v1/review/'
#         user = create_user_factory()
#         self.movie = create_movie_factory(user=user)
#         self.instance = create_review_factory(movie=self.movie, user=user)
#         # self.instances = create_reviews_set(movie=self.movie)
#         self.client.force_authenticate(user=user)

#         self.factory = APIRequestFactory()
#         request = self.factory.get(self.url)
#         self.context = {'request': request}
#         self.serializer = RecursiveSerializer(
#             instance=self.instance, context=self.context)

    # TODO: finish this test.
    # def test_to_representation(self):
    #     data = self.serializer.to_representation(self.instance)
