from .models import Ingredient, IngredientRecipe, Recipe


def add_ingredients(ingredients_data: list, recipe: Recipe) -> Recipe:
    ingredients_list = []
    ingredients = Ingredient.objects.filter(
        id__in=[data.get('id') for data in ingredients_data]
    )

    for ingredient_data in ingredients_data:
        ingredients_list.append(IngredientRecipe(
            recipe=recipe,
            ingredients=ingredients.get(id=ingredient_data.get('id')),
            amount=ingredient_data.get('amount')
        ))
    IngredientRecipe.objects.bulk_create(ingredients_list)
    return recipe
