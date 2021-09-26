from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Favorite, Recipe, ShoppingCart, Tag, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model
from users.serializers import UserDetailSerializers
from drf_extra_fields.fields import Base64ImageField

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


class TagDetailSerializer(serializers.ModelSerializer):
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


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeDetailSerializer(serializers.ModelSerializer):
    
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagListSerializer(read_only=True, many=True)
    image = Base64ImageField()

    author = UserDetailSerializers(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        many=True,
        read_only=True,
        source='recipeingredient_set'
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        else:
            return Favorite.objects.filter(
                user=request.user,
                favorite_recipe=obj
            ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        else:
            return ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
    
    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient_obj in ingredients:
            if int(ingredient_obj['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Колличество ингредиента должно'
                                    'быть больше 0')
                })
        data['ingredients'] = ingredients

        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients_validate = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=author,
            **validated_data
        )
        tags_obj = self.initial_data.get('tags')
        recipe.tags.set(tags_obj)

        for ingredient in ingredients_validate:
            
            RecipeIngredient.objects.create(
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
        return recipe
    
    def update(self, instance, validated_data):
        ingredient_get = validated_data.get('ingredients')
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
        RecipeIngredient.objects.filter(recipe=instance).all().delete()

        for ingredient in ingredient_get:
            ingredient_obj = RecipeIngredient.objects.create(
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=instance
            )
            ingredient_obj.save()
        
        instance.save()
        return instance
