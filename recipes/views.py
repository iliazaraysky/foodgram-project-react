from rest_framework import generics, permissions, filters, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from recipes.models import Recipe, Tag, Ingredient, Favorite
from recipes.serializers import (RecipeDetailSerializer,
                                 RecipeListSerializer,
                                 TagDetailSerializer,
                                 TagListSerializer,
                                 IngredientsDetailSerializer,
                                 IngredientsListSerializer,
                                 )

from recipes.permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404


# class APIRecipeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeDetailSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
#     lookup_field = 'pk'

class APIRecipe(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = RecipeDetailSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        return queryset.all()

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated]
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


class APIRecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
