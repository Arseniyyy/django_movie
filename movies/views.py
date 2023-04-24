from django.db.models import Q, Count, Sum, F
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)

from movies.services import get_client_ip
from movies.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from movies.models import Actor, Genre, Movie, Review, Rating
from movies.serializers import (ReviewCreateUpdateDestroySerializer,
                                RatingCreateSerializer,
                                ActorListSerializer,
                                GenreSerializer,
                                ReviewSerializer,
                                MovieListRetrieveSerializer,
                                MovieSerializer)


class MovieListCreateViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend,)

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
            average_rating=Sum(F('ratings__star')) / Count(F('ratings'))
        )
        # search_query = self.request.query_params.get('q', None)
        # start_year = self.request.query_params.get('start_year', None)
        # end_year = self.request.query_params.get('end_year', None)

        # if search_query:
        #     # check if q is a digit
        #     if search_query.isdigit():
        #         search_query = int(search_query)
        #         queryset = queryset.filter(
        #             Q(year=search_query) |
        #             Q(budget=search_query)
        #         )

        #     # check if q is type of str
        #     else:
        #         queryset = queryset.filter(
        #             Q(title__icontains=search_query) |
        #             Q(description__icontains=search_query) |
        #             Q(actors__name__icontains=search_query) |
        #             Q(directors__name__icontains=search_query) |
        #             Q(country__icontains=search_query) |
        #             Q(genres__name__icontains=search_query) |
        #             Q(category__name__icontains=search_query)
        #         )
        # # check if start_year and end_year are not None and filter the previous queryset with new values
        # if start_year and end_year:
        #     queryset = queryset.filter(year__range=(start_year, end_year))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class RatingListCreateViewSet(viewsets.ModelViewSet):
    serializer_class = RatingCreateSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # queryset is a set of all ratings made by the current user
        queryset = Rating.objects.filter(ip=get_client_ip(self.request))
        rating_star_start = self.request.query_params.get('rating_star_start')
        rating_star_end = self.request.query_params.get('rating_star_end')

        if rating_star_start and rating_star_end:
            queryset = queryset.filter(star__range=(rating_star_start, rating_star_end))
        return queryset

    def create(self, request: Request, *args, **kwargs):
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
    """This view is used for printing all actors and creating a new one."""

    serializer_class = ActorListSerializer
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
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

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]


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
