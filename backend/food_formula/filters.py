from django_filters import rest_framework as rest_framework_filter
from rest_framework.filters import SearchFilter

from .models import Recipe
from .models import User


class RecipeFilter(rest_framework_filter.FilterSet):
    """
    Настройка фильтров модели рецептов.
    """
    author = rest_framework_filter.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = rest_framework_filter.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = rest_framework_filter.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = rest_framework_filter.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        """
        Метод обработки фильтров параметра is_favorited.
        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """
        Метод обработки фильтров параметра is_in_shopping_cart.
        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    """
    Настройка фильтра поиска модели продуктов.
    """
    search_param = 'name'
