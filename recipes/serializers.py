from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model

User = get_user_model()


class RepresentAuthor(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = AuthorSerializer(obj)
        return serializer.data


class RepresentTags(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = TagSerializer(obj)
        return serializer.data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', )


class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    author = RepresentAuthor(
        slug_field='id',
        queryset=User.objects.all(),
        required=False
    )

    tags = RepresentTags(
        slug_field='slug',
        queryset=Tag.objects.all(),
        required=False,
        many=True
    )

    ingredients = IngredientSerializer(
        source='recipeingredient_set',
        many=True
    )

    image = serializers.ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'name', 'image',
                  'text', 'cooking_time')


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
