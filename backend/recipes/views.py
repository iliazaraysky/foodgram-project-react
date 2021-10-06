from .filters import IngredientFilter, RecipeFilter
from django.http.response import HttpResponse
from django.db.models import Sum
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Recipe,
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
        shopping_list = []
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user__username=user)
        shopping_cart_data = shopping_cart.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(
            total_amount=Sum(
                'recipe__recipeingredient__amount'
            )
        ).order_by(
            'recipe__ingredients__name'
        )
        for item in shopping_cart_data:
            shopping_list.append(
                f'{item["recipe__ingredients__name"]}'
                f' {item["total_amount"]}'
                f' {item["recipe__ingredients__measurement_unit"]} \n'
            )

        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response[
            'Content-Discription'] = 'attachment; filename="product_list.txt"'

        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
