from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User, models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Текст')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.IntegerField(verbose_name='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент-рецепт'
        verbose_name_plural = 'Ингредиент-рецепты'
        constraints = [models.UniqueConstraint(
            fields=['ingredients', 'recipe'],
            name='Unique IngredientRecipe'
        )]

    def __str__(self):
        return f'{self.ingredients} ({self.amount}) -> {self.recipe}'


class RecipeFollow(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        'is_favorite',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        'favorite',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='Unique RecipeFollow'
        )]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        'cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        'cart_of',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='Unique Cart'
        )]

    def __str__(self):
        return f'Cart of {self.user} with {self.recipe}'
