from rest_framework import serializers
from recipes.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
