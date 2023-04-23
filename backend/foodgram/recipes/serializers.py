from rest_framework.serializers import ModelSerializer
from .models import Ingredient


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

