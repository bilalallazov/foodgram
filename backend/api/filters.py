from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ()

    def filter_is_favorited(self, queryset, name, value):
        if value is None:
            return queryset
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if int(value) == 1 else queryset
        if int(value) == 1:
            return queryset.filter(favorites__user=user).distinct()
        return queryset.exclude(favorites__user=user).distinct()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value is None:
            return queryset
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if int(value) == 1 else queryset
        if int(value) == 1:
            return queryset.filter(shopping_cart__user=user).distinct()
        return queryset.exclude(shopping_cart__user=user).distinct()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
