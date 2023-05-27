import rest_framework

from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from djoser.views import UserViewSet
from djoser.conf import settings
from djoser.compat import get_user_email
from dotenv import load_dotenv

from users.serializers import UserPatchSerializer, UserRetrieveSerializer


load_dotenv()


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
        data = {
            "id": current_user.pk,
            "email": current_user.email,
        }
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args, **kwargs):
        current_user = request.user
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=current_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CustomActivationViewSet(UserViewSet):
    """
    Verificates a user's email and toggles `is_active` to `True` if has been registered successfully.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @action(['post'], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user=user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        email = user.email
        response_data = {'email': email, 'access': access_token, 'refresh': refresh_token}

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(response_data, status=status.HTTP_200_OK)
