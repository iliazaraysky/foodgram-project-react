from django.http.response import HttpResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from recipes.models import Recipe, RecipeIngredient, Tag, Ingredient, Favorite, ShoppingCart
from recipes.serializers import (RecipeDetailSerializer,
                                 TagDetailSerializer,
                                 TagListSerializer,
                                 IngredientsDetailSerializer,
                                 IngredientsListSerializer,
                                 )

from recipes.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404


class APIRecipe(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        return queryset.all()

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        url_path='favorite',
    )
    def favorite(self, request, pk):
        if request.method == 'GET':
            favorite_recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(
                favorite_recipe=favorite_recipe,
                user=request.user
            )
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite_recipe = get_object_or_404(
                Favorite,
                favorite_recipe__id=pk,
                user=request.user
            )
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        url_path='shopping_cart'
    )
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(
                recipe=recipe,
                user=request.user
            )
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(
                ShoppingCart,
                recipe__id=pk,
                user=request.user
            )
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.shoppingcart_set.all()
        ingredient_amount_dict = {}
        ingredient_measurement_unit_dict = {}

        for obj in shopping_cart:
            recipe = obj.recipe
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

            for ingredient in recipe_ingredients:
                ingredient_name = ingredient.ingredient
                # ingredient_for_recipe = ingredient.recipe
                ingredient_amount = ingredient.amount
                ingredient_measurement_unit = ingredient.ingredient.measurement_unit
                if ingredient_name in ingredient_amount_dict:
                    ingredient_amount_dict[ingredient_name] = ingredient_amount_dict[ingredient_name] + ingredient_amount
                else:
                    ingredient_amount_dict[ingredient_name] = ingredient_amount
                    ingredient_measurement_unit_dict[ingredient_name] = ingredient_measurement_unit
        
        list_of_what_to_buy = ''
        for obj in ingredient_amount_dict.keys():
            list_of_what_to_buy += f'{obj}: {ingredient_amount_dict[obj]} {ingredient_measurement_unit_dict[obj]}\n'


        response = HttpResponse(list_of_what_to_buy, content_type='text/plain')
        filename = 'what_to_buy.txt'
        response['Content-Disposition'] = ['attachment; filename={0}'.format(filename)]
        return HttpResponse(response)


class APITagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'pk'


class APITagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, list):
                kwargs['many'] = True
        return super(APITagList, self).get_serializer(*args, **kwargs)

    class Meta:
        ordering = ('id', )


class APIIngredientsDetail(generics.RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsDetailSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'pk'


class APIIngredientsList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsListSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, list):
                kwargs['many'] = True
        return super(APIIngredientsList, self).get_serializer(*args, **kwargs)

    class Meta:
        ordering = ('id', )
