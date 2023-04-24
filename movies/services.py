from rest_framework.request import Request
from django_filters import rest_framework as filters

from movies.models import Movie, Rating


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ('genres', 'year',)


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
    return Rating.objects.create(**validated_data)
