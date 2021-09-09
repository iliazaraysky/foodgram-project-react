from rest_framework import mixins, generics, viewsets, filters, permissions
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django_filters.rest_framework import DjangoFilterBackend


class APIRecipeList(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
