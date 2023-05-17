from django_filters.rest_framework import FilterSet, filters

from .models import Recipe


class RecipeFilters(FilterSet):
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='exact')
    author = filters.NumberFilter(field_name='author', lookup_expr='exact')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_cart')

    class Meta:
        model = Recipe
        fields = ['tags']

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(is_favorite__user=self.request.user)
        return queryset

    def filter_is_in_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)
        return queryset
