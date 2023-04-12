from rest_framework import serializers
from django.core.exceptions import ValidationError

from movies.models import (
    Movie,
    Rating,
    Star,
    Review,
    Actor,
    Genre
)
from movies.services import create_rating


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            if data == "none":
                return "no image"
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except ValidationError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class MovieSerializer(serializers.ModelSerializer):
    poster = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Movie
        fields = ('id',
                  'title',
                  'url',
                  'tagline',
                  'category',
                  'poster',
                  'directors')


class MovieListRetrieveSerializer(serializers.ModelSerializer):
    """List of movies"""
    poster = Base64ImageField(max_length=None, use_url=True)
    directors = serializers.SlugRelatedField(
        slug_field='name', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id',
                  'title',
                  'url',
                  'tagline',
                  'category',
                  'poster',
                  'directors')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewCreateUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children', 'user', 'movie')

    def get_related_field(self, model_field):
        return ReviewSerializer()


class StarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('value',)


class RatingCreateSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return create_rating(**validated_data)

    class Meta:
        model = Rating
        fields = ('star', 'movie', 'ip')


class ActorSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Actor
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
