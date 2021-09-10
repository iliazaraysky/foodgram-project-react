from rest_framework import generics, permissions
from recipes.models import Recipe, Tag, Ingredient
from recipes.serializers import (RecipeDetailSerializer,
                                 RecipeListSerializer,
                                 TagDetailSerializer,
                                 TagListSerializer,
                                 IngredientsDetailSerializer,
                                 IngredientsListSerializer)


class APIRecipeDetail(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class APIRecipeList(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APITagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class APITagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class APIIngredientsDetail(generics.RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class APIIngredientsList(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
