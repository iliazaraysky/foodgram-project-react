from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from .models import Recipe, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='favorite')
    is_in_shopping_cart = filters.BooleanFilter(method='shoppingcart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorite__user=user)
        return queryset

    def shoppingcart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(shoppingcart__user=user)
        return queryset
