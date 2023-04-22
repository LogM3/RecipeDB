from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import CharField

from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

