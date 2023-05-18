from .models import IngredientRecipe, Recipe


def add_ingredients(ingredients_data: list, recipe: Recipe) -> Recipe:
    ingredients_list = []

    for ingredient_data in ingredients_data:
        ingredients_list.append(IngredientRecipe(
            recipe=recipe,
            ingredient_id=ingredient_data.get('id'),
            amount=ingredient_data.get('amount')
        ))
    IngredientRecipe.objects.bulk_create(ingredients_list)
    return recipe
