from rest_framework import serializers
from recipes.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
