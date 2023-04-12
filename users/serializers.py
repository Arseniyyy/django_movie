from rest_framework import serializers
from users.models import CustomUser


class UserCreateResponseSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=None)

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'access')
