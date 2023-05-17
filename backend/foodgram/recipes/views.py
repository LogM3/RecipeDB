from django.db.models import Sum
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
from rest_framework.request import HttpRequest as Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.permissions import IsAuthor
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

    def __add_or_remove(
            self,
            request: Request,
            recipe: Recipe,
            obj_to_create,
            error_context_msg: str
    ) -> Response:

        is_exists = obj_to_create.objects.filter(
            user=request.user, recipe=recipe
        ).exists()
        if request.method == 'POST':
            if is_exists:
                return Response(
                    f'You are already {error_context_msg} this recipe',
                    status=HTTP_400_BAD_REQUEST
                )
            obj_to_create.objects.create(user=request.user, recipe=recipe)
            return Response(
                ShortRecipeSerializer(recipe).data, status=HTTP_201_CREATED
            )
        if not is_exists:
            return Response(
                f'You are not {error_context_msg} this recipe',
                status=HTTP_400_BAD_REQUEST
            )
        with atomic():
            obj_to_create.objects.filter(
                recipe=recipe,
                user=request.user
            ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        return self.__add_or_remove(
            self.request,
            get_object_or_404(Recipe, pk=pk),
            RecipeFollow,
            'liked'
        )

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        return self.__add_or_remove(
            self.request,
            get_object_or_404(Recipe, pk=pk),
            Cart,
            'put to cart'
        )

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_total = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__cart__user=request.user
        ).order_by('ingredients__name').values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(total_amount=Sum('amount'))

        for ingredient in ingredients:
            ingredients_total[ingredient.get('ingredients__name')] = {
                'measurement_unit': ingredient.get(
                    'ingredients__measurement_unit'
                ),
                'amount': ingredient.get('total_amount')
            }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment;'
                                           ' filename="shopping_cart.pdf"')
        pdfmetrics.registerFont(TTFont('pacifico', 'Pacifico.ttf', 'UTF-8'))
        page = Canvas(response)
        page.setFont('pacifico', size=24)
        page.drawString(190, 800, 'Список ингредиентов')
        page.setFont('pacifico', size=21)
        y_axis = 740
        x_axis = 75
        for count, (name, data) in enumerate(ingredients_total.items(), 1):
            page.drawString(
                x_axis,
                y_axis,
                f'{count}. {name} - {data.get("amount")} '
                f'{data.get("measurement_unit")}.'
            )
            y_axis -= 38

        page.showPage()
        page.save()
        return response
