import os

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from djoser.serializers import UserCreateSerializer, UserSerializer
from dotenv import load_dotenv

from users.models import CustomUser
from users.serializers import TokenUserObtainSerializer
from users.services import get_access_token


load_dotenv()

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    list_serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    jwt_url = f'{os.getenv("LOCALHOST_URL")}/auth/jwt/token/'

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.list_serializer_class
        else:
            return self.create_serializer_class

    def create(self, request, *args, **kwargs):
        """
        Creates a user and returns their email, access, and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {'email': request.data['email'], 'password': request.data['password']}
        token_pair = get_access_token(self.jwt_url, data=data)
        token_user_data = {**token_pair, 'email': serializer.data['email']}
        token_pair_serializer = TokenUserObtainSerializer(token_user_data)
        return Response(token_pair_serializer.data, status=status.HTTP_201_CREATED)
    

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = ()
