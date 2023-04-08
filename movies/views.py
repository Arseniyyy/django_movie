from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_simplejwt.authentication import JWTAuthentication

from movies.permissions import (IsAdminOrReadOnly,
                                IsOwnerOrReadOnly)
from movies.models import (Actor, Genre, Movie,
                           Review, Rating, Star,)
from movies.serializers import (ReviewCreateUpdateDestroySerializer,
                                CreateRatingSerializer,
                                CreateStarSerializer,
                                ActorSerializer,
                                GenreSerializer,
                                ReviewSerializer,
                                MovieListRetrieveSerializer,
                                MovieSerializer)


class MovieListCreateViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.filter(is_draft=False).all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        serializer = MovieListRetrieveSerializer(self.queryset, many=True)
        return Response(serializer.data)


class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListRetrieveSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    list_serializer_class = ReviewSerializer
    create_serializer_class = ReviewCreateUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)
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


class CreateStarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = CreateStarSerializer


class ListCreateRatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def create(self, request: Request, *args, **kwargs):
        serializer = CreateRatingSerializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(ip=self.get_client_ip(self.request))


class ActorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = Actor.objects.all().order_by('-first_creation_time')
        return queryset


class ActorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)


class GenreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
