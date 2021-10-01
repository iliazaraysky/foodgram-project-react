from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import (Favorite,
                            Recipe,
                            ShoppingCart,
                            Tag,
                            Ingredient,
                            RecipeIngredient)
from django.contrib.auth import get_user_model
from users.serializers import CustomUserSerializer
from drf_extra_fields.fields import Base64ImageField
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class MinRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')
        read_only_fields = ('id', 'name', 'cooking_time', 'image')


class RecipeDetailSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagDetailSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True
    )

    cooking_time = serializers.IntegerField(
        validators=[MinValueValidator(
            limit_value=1,
            message='Время приготовления не может быть меньше 1')]
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Favorite.objects.filter(
                favorite_recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                recipe=obj, user=request.user).exists()

    def validate(self, data):
        ingredients = self.initial_data.pop('ingredients')
        for ingredient_model in ingredients:
            if int(ingredient_model['amount']) < 0:
                raise ValidationError('Колличество ингредиента должно'
                                      'быть больше 0')

        count_unique_ingreds = set([item['id'] for item in ingredients])
        if len(count_unique_ingreds) != len(ingredients):
            raise ValidationError(
                'В рецепте не может быть два одинаковых ингредиента'
            )
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_validate = validated_data.pop('ingredients')
        tags_data = self.initial_data.pop('tags')
        recipe = Recipe.objects.create(
            author=get_object_or_404(
                User, id=validated_data.pop('author').id),
            image=image, **validated_data
        )
        for tag_ in tags_data:
            recipe.tags.add(get_object_or_404(Tag, id=tag_))

        for ingredient in ingredients_validate:
            amount = ingredient.pop('amount')
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient.pop('id')
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        instance.tags.clear()
        tags_obj = self.initial_data.get('tags')
        instance.tags.set(tags_obj)

        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients_validate = validated_data.pop('ingredients')

        for ingredient in ingredients_validate:
            amount = ingredient.pop('amount')
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient.pop('id')
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=instance, amount=amount
            )
        instance.save()
        return instance


class FavoriteCreateSerializer(serializers.ModelSerializer):
    queryset = Recipe.objects.all()

    class Meta:
        model = Favorite
        fields = ('user', 'favorite_recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'favorite_recipe'),
                message='Этот рецепт уже в избранном'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return MinRecipeSerializer(
            instance.favorite_recipe,
            context={'request': request}).data


class CartCreateSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже в корзинe'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return MinRecipeSerializer(
            instance.recipe,
            context={'request': request}).data
