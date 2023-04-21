from rest_framework.serializers import CharField, ModelSerializer
from djoser.serializers import UserCreateSerializer

from .models import User


class CreateUserSerializer(UserCreateSerializer):
    first_name = CharField(max_length=25, required=True)
    last_name = CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

