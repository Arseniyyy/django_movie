from rest_framework import generics
from rest_framework.response import Response
from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings

from users.models import CustomUser
from users.services import create_user
from users.serializers import UserCreateResponseSerializer


class ListCreateUserAPIView(generics.ListCreateAPIView):
    list_serializer = UserSerializer
    create_serializer = UserCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.list_serializer
        else:
            return self.create_serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data)  # UserCreateSerializer
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
