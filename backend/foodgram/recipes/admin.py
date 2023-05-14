from django.contrib import admin

from .models import Cart, Ingredient, IngredientRecipe, Recipe, RecipeFollow


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ['name']


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['author', 'name', 'tags']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeFollow)
admin.site.register(IngredientRecipe)
admin.site.register(Cart)
