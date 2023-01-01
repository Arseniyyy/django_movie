from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import viewsets

from movies.models import (Actor, Movie,
                           Review,
                           Rating,
                           Star)
from movies.serializers import (MovieSerializer,
                                ReviewCreateSerializer,
                                CreateRatingSerializer,
                                CreateStarSerializer,
                                ActorSerializer)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


class CreateStarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = CreateStarSerializer


class ListCreateRatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

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
            serializer.save(ip=self.get_client_ip(request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
