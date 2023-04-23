from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from .models import Ingredient
from .serializers import IngredientsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name']


