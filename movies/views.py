from django.db.models import Q, Count, Sum, F, IntegerField, Avg
from django.db.models.functions import Cast
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,)

from movies.services import get_client_ip
from movies.filters import MovieFilter, ActorFilter, RatingFilter
from movies.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from movies.models import Actor, Genre, Movie, Review, Rating
from movies.pagination import MovieListCreateAPIViewPagination
from movies.serializers import (ReviewCreateUpdateDestroySerializer,
                                RatingSerializer,
                                ActorListSerializer,
                                GenreSerializer,
                                ReviewSerializer,
                                MovieListRetrieveSerializer,
                                MovieSerializer,)


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.filter()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter
    pagination_class = MovieListCreateAPIViewPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Implements a search function for Movie's fields:
        `title`, `year`,
        `description`, `actors`,
        `world_premiere`, `country`,
        `genres`, `category`.
        """
        queryset = Movie.objects.filter(is_draft=False).order_by('-id').annotate(
            rating_user=Count('ratings', filter=Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            average_rating=Sum(F('ratings__total_rating')) / Count(F('ratings'))
        )
        return queryset


class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListRetrieveSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    list_serializer_class = ReviewSerializer
    create_serializer_class = ReviewCreateUpdateDestroySerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.list_serializer_class
        if self.request.method == "POST":
            return self.create_serializer_class
        else:
            return self.create_serializer_class


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    retrieve_serializer_class = ReviewSerializer
    serializer_class = ReviewCreateUpdateDestroySerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.retrieve_serializer_class
        else:
            return self.serializer_class


class RatingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    authentication_classes = (JWTAuthentication,)
    filterset_class = RatingFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Gets the queryset for this view and counts an average rating for the provided movie.
        """
        # queryset is a set of all ratings made by the current user
        queryset = Rating.objects.filter(ip=get_client_ip(self.request))
        queryset = self.filter_queryset(queryset=queryset)
        return queryset

    def post(self, request: Request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class RatingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewCreateUpdateDestroySerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ActorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ActorListSerializer
    authentication_classes = (JWTAuthentication,)
    filterset_class = ActorFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Gets the queyrset depending on query parameters."""
        queryset = Actor.objects.all().order_by('-first_creation_time')
        search_query = self.request.query_params.get('q', None)
        start_age = self.request.query_params.get('start_age', None)
        end_age = self.request.query_params.get('end_age', None)

        if search_query:
            if search_query.isdigit():
                search_query = int(search_query)
                queryset = queryset.filter(age=search_query)
            else:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query)
                )
        if start_age and end_age:
            # here we find an actor with the age varying from start_age to end_age
            queryset = queryset.filter(age__range=(start_age, end_age))
        return queryset


class ActorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    lookup_field = 'name'

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]


class GenreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]
