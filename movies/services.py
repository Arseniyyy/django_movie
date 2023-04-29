from django.db.models import F
from rest_framework.request import Request

from movies.models import Movie, Rating


def get_client_ip(request: Request):
    """Gets the user's ip when logs in."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_movie(**validated_data):
    return Movie.objects.create(**validated_data)


def create_rating(**validated_data):
    storyline_rating = validated_data['storyline_rating']
    acting_rating = validated_data['acting_rating']
    cinematography_rating = validated_data['cinematography_rating']

    # total_rating = (F('storyline_rating') + F('acting_rating') + F('cinematography_rating')) / 3
    total_rating = (storyline_rating + acting_rating + cinematography_rating) / 3
    return Rating.objects.create(**validated_data, total_rating=total_rating)
