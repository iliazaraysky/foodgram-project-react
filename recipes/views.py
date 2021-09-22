from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from recipes.models import Recipe, Tag, Ingredient, Favorite
from recipes.serializers import (RecipeDetailSerializer,
                                 RecipeListSerializer,
                                 TagDetailSerializer,
                                 TagListSerializer,
                                 IngredientsDetailSerializer,
                                 IngredientsListSerializer,
                                 )

from recipes.permissions import IsAdminOrReadOnly


class APIRecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'pk'


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
