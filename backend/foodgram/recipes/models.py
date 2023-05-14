from django.db import models
from django.core.validators import MinValueValidator

from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(User, models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/images')
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredients = models.ForeignKey(Ingredient, models.CASCADE)
    recipe = models.ForeignKey(Recipe, models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredients} ({self.amount}) -> {self.recipe}'


class RecipeFollow(models.Model):
    recipe = models.ForeignKey(Recipe, models.CASCADE, 'is_favorite')
    user = models.ForeignKey(User, models.CASCADE, 'favorite')

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'cart')
    recipe = models.ForeignKey(Recipe, models.CASCADE, 'cart_of')

    def __str__(self):
        return f'Cart of {self.user} with {self.recipe}'

