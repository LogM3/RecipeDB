from core.permissions import IsAuthor
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import RecipeFilters
from .models import Cart, Ingredient, IngredientRecipe, Recipe, RecipeFollow
from .serializers import (CreateRecipeSerializer, IngredientsSerializer,
                          ReadOnlyRecipeSerializer, ShortRecipeSerializer)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilters
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyRecipeSerializer
        return CreateRecipeSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsAuthor()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        serializer = ReadOnlyRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = ReadOnlyRecipeSerializer(
            serializer.save(),
            context={'request': request}
        )
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_favorite = RecipeFollow.objects.filter(
            user=request.user, recipe=recipe
        )
        if request.method == 'POST':
            if is_favorite:
                return Response(
                    'You are already liked this recipe',
                    status=HTTP_400_BAD_REQUEST
                )
            RecipeFollow.objects.create(user=request.user, recipe=recipe)
            return Response(
                ShortRecipeSerializer(recipe).data, status=HTTP_201_CREATED
            )

        if not is_favorite:
            return Response(
                'You are not liked this recipe',
                status=HTTP_400_BAD_REQUEST
            )
        with atomic():
            RecipeFollow.objects.filter(recipe=recipe, user=user).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_in_cart = Cart.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if is_in_cart:
                return Response(
                    'You are already added this recipe to your cart',
                    status=HTTP_400_BAD_REQUEST
                )
            Cart.objects.create(user=user, recipe=recipe)
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=HTTP_201_CREATED
            )

        if not is_in_cart:
            return Response(
                'You have not added this recipe to your cart yet.',
                status=HTTP_400_BAD_REQUEST
            )
        with atomic():
            is_in_cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        def get_ingredient_filed(field: str) -> int:
            ingredients_indexes = {
                'name': 0,
                'measurement_unit': 1,
                'amount': 2
            }
            return ingredients_indexes.get(field)

        ingredients_total = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__cart_of__user=request.user
        ).values_list(
            'ingredients__name',
            'ingredients__measurement_unit',
            'amount'
        )
        for ingredient in ingredients:
            name = ingredient[get_ingredient_filed('name')]
            amount = ingredient[get_ingredient_filed('amount')]

            if ingredient in ingredients_total:
                ingredients_total[name]['amount'] += amount
            else:
                measurement_unit = ingredient[get_ingredient_filed(
                    'measurement_unit'
                )]
                ingredients_total[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment;'
                                           ' filename="shopping_cart.pdf"')
        pdfmetrics.registerFont(TTFont('pixel_font', 'PixelFont.ttf', 'UTF-8'))
        page = Canvas(response)
        page.setFont('pixel_font', size=18)
        page.drawString(150, 800, 'Список ингредиентов')
        page.setFont('pixel_font', size=14)
        y_axis = 750
        x_axis = 75
        for count, (name, data) in enumerate(ingredients_total.items(), 1):
            page.drawString(
                x_axis,
                y_axis,
                f'{count}){name} - {data.get("amount")} '
                f'{data.get("measurement_unit")}.'
            )
            y_axis -= 30

        page.showPage()
        page.save()
        return response
