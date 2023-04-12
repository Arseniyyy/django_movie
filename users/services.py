from users.models import CustomUser


def create_user(**validated_data):
    return CustomUser.objects.create(**validated_data)
