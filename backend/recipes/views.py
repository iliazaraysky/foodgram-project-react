from .filters import IngredientFilter, RecipeFilter
from django.http.response import HttpResponse
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Recipe,
    RecipeIngredient,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart
)
from .serializers import (
    IngredientsDetailSerializer,
    TagDetailSerializer,
    RecipeDetailSerializer,
    FavoriteCreateSerializer,
    CartCreateSerializer
)
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404


class APIIngredients(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsDetailSerializer
    pagination_class = None
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ['^name']


class APITags(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = None


class APIRecipe(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    filter_class = RecipeFilter
    queryset = Recipe.objects.all()


    @action(detail=True, permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk=None):
        data = {
            'user': request.user.id,
            'favorite_recipe': pk
        }
        serializer = FavoriteCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        favorite = get_object_or_404(
            Favorite,
            user=user,
            favorite_recipe_id=pk
        )
        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = CartCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        ShoppingCart.objects.filter(
            user=user, recipe=get_object_or_404(Recipe, id=pk)).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.shoppingcart_set.all()
        shopping_cart_data = {}
        for item_recipe in shopping_cart:
            ingredients_from_cart = RecipeIngredient.objects.filter(
                recipe=item_recipe.recipe
            )
            for ingredient_obj in ingredients_from_cart:
                name = ingredient_obj.ingredient.name
                amount = ingredient_obj.amount
                measurement_unit = ingredient_obj.ingredient.measurement_unit
                if name in shopping_cart_data:
                    shopping_cart_data[name]['amount'] += amount
                else:
                    shopping_cart_data[name] = {
                        'amount': amount,
                        'measurement_unit': measurement_unit
                    }
        shopping_list = ([f'{item} - {shopping_cart_data[item]["amount"]} '
                          f'{shopping_cart_data[item]["measurement_unit"]} \n'
                          for item in shopping_cart_data])
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response[
            'Content-Discription'] = 'attachment; filename="product_list.txt"'

        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
