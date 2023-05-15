from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import CharField, SerializerMethodField

from recipes.models import Recipe
from recipes.serializers import ShortRecipeSerializer


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


class CustomUserSerializerWithRecipes(CustomUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = READ_ONLY_USER_FIELDS

    def get_recipes(self, obj):
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            return ShortRecipeSerializer(
                Recipe.objects.filter(author=obj)[:int(limit)],
                many=True
            ).data
        return ShortRecipeSerializer(
            Recipe.objects.filter(author=obj),
            many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
