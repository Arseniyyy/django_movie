from rest_framework import serializers


class TokenUserObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    refresh = serializers.CharField(max_length=None)
    access = serializers.CharField(max_length=None)
