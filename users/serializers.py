from rest_framework import serializers
from djoser.serializers import UserSerializer

from users.models import CustomUser


class TokenUserObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    refresh = serializers.CharField(max_length=None)
    access = serializers.CharField(max_length=None)


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id",
                  "email")


class UserPatchSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ("id",
                  "email")
