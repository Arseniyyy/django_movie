import os

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from djoser.serializers import UserCreateSerializer, UserSerializer
from dotenv import load_dotenv

from users.models import CustomUser
from users.serializers import TokenUserObtainSerializer, UserPatchSerializer, UserRetrieveSerializer
from users.services import get_access_token


load_dotenv()

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    list_serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    jwt_url = f'{os.getenv("LOCALHOST_URL")}/auth/jwt/token/'

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = (IsAuthenticated,)
        elif self.request.method == "POST":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.list_serializer_class
        else:
            return self.create_serializer_class

    def create(self, request, *args, **kwargs):
        """
        Creates a user and returns his email, access, and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {'email': request.data['email'], 'password': request.data['password']}
        token_pair = get_access_token(self.jwt_url, data=data)
        token_user_data = {**token_pair, 'email': serializer.data['email']}
        token_pair_serializer = TokenUserObtainSerializer(token_user_data)
        return Response(token_pair_serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    retrieve_serializer_class = UserRetrieveSerializer
    patch_serializer_class = UserPatchSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.retrieve_serializer_class
        elif self.request.method == "PATCH":
            return self.patch_serializer_class

    def get(self, request: Request):
        current_user = request.user
        data = {**request.data, "id": current_user.pk,}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args, **kwargs):
        current_user = request.user
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=current_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
