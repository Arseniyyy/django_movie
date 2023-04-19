import requests

from users.models import CustomUser


def create_user(**validated_data):
    return CustomUser.objects.create(**validated_data)


def get_access_refresh_token(url, email, password):
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url=url, data=data)
    response = response.json()
    token_pair = {
        'refresh': response['refresh'],
        'access': response['access'],
    }
    return token_pair
