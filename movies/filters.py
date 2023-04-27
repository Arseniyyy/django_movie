from django_filters import rest_framework as filters

from movies.models import Actor, Movie, Rating


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    directors = CharFilterInFilter(field_name='actors__name', lookup_expr='icontains')
    actors = CharFilterInFilter(field_name='actors__name', lookup_expr='icontains')
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    country = filters.CharFilter(field_name='country', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    year = filters.RangeFilter()

    class Meta:
        model = Movie
        exclude = ('poster',)


class ActorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    age = filters.RangeFilter()

    class Meta:
        model = Actor
        fields = ('name', 'age',)


class RatingFilter(filters.FilterSet):
    star = filters.RangeFilter()
    
    class Meta:
        model = Rating
        fields = ('star',)
