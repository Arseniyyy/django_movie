import requests

from users.models import CustomUser


def create_user(**validated_data):
    return CustomUser.objects.create(**validated_data)


def get_access_token(url, data):
    response = requests.post(url=url, data=data)
    response = response.json()
    token_pair = {
        'refresh': response['refresh'],
        'access': response['access'],
    }
    return token_pair
