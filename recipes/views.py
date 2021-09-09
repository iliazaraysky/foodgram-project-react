from rest_framework.response import Response
from rest_framework.views import APIView


from recipes.models import Recipe
from recipes.serializers import RecipeListSerializers


class RecipecListView(APIView):
    def get(self, request):
        recipes = Recipe.objects.filter(draft=False)
        serializer = RecipeListSerializers(recipes, many=True)
        return Response(serializer.data)
