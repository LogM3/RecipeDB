from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import CharField, SerializerMethodField

from .models import User


READ_ONLY_USER_FIELDS = [
    'email',
    'id',
    'username',
    'first_name',
    'last_name',
    'is_subscribed',
    'recipes',
    'recipes_count'
]
COMMON_FIELDS_END_INDEX = -2


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = READ_ONLY_USER_FIELDS[:COMMON_FIELDS_END_INDEX]

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous or current_user == obj:
            return False
        return current_user.subscribed.filter(author=obj).exists()
