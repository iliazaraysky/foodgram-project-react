from rest_framework import serializers

from recipes.models import Recipe


class RecipeListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'
