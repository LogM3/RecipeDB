import base64

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ListField,
    DictField,
    HiddenField,
    CurrentUserDefault,
    ReadOnlyField,
    ImageField
)
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from django.core.files.base import ContentFile
from rest_framework.serializers import ValidationError, SerializerMethodField

from .models import Ingredient, Recipe, IngredientRecipe, RecipeFollow, Cart
from tags.models import Tag
from users.serializers import CustomUserSerializer
from tags.serializers import TagSerializer

RECIPE_FIELDS = (
    'id',
    'tags',
    'author',
    'ingredients',
    'name',
    'image',
    'text',
    'cooking_time',
    'is_favorited',
    'is_in_shopping_cart'
)
RECIPE_CREATE_CUTOFF_INDEX = -2


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(ModelSerializer):
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            _format, _imgstr = data.split(';base64,')
            ext = _format.split('/')[-1]
            data = ContentFile(base64.b64decode(_imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ReadOnlyRecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(many=False, read_only=True)
    ingredients = IngredientsRecipeSerializer(
        many=True, source='ingredientrecipe_set'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = RECIPE_FIELDS

    def get_is_favorited(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False
        return RecipeFollow.objects.filter(
            recipe=obj,
            user=user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False
        return Cart.objects.filter(
            recipe=obj,
            user=user
        ).exists()


class ShortRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class CreateRecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = HiddenField(default=CurrentUserDefault())
    ingredients = ListField(child=DictField(), write_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = RECIPE_FIELDS[:RECIPE_CREATE_CUTOFF_INDEX]

    def validate_ingredients(self, ingredients_data):
        for ingredient in ingredients_data:
            keys = ingredient.keys()
            if 'id' not in keys or 'amount' not in keys:
                raise ValidationError('Invalid ingredient data')
            if int(ingredient.get('amount')) < 1:
                raise ValidationError('Amount must be greater or equal 1')
        return ingredients_data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        for ingredient_data in ingredients_data:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_data.get('id')
            )
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredients=ingredient,
                amount=ingredient_data.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        instance.tags.set(validated_data.get('tags'))
        with atomic():
            instance.ingredientrecipe_set.all().delete()
            for ingredient_data in validated_data.get('ingredients'):
                ingredient = get_object_or_404(
                    Ingredient, id=ingredient_data.get('id')
                )
                IngredientRecipe.objects.create(
                    recipe=instance,
                    ingredients=ingredient,
                    amount=ingredient_data.get('amount')
                )
        return instance

