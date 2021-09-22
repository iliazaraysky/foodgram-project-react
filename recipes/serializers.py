from django.core import exceptions
from rest_framework import fields, serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data  = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = '%s.%s' % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)
    
    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension


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
    
    name = serializers.CharField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_fields(self, *args, **kwargs):
        fields = super(RecipeDetailSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == 'PUT':
            fields['name'].required = False
            fields['author'].required = False
            fields['tags'].required = False
        return fields


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

    image = Base64ImageField(
        max_length = None,
        use_url = True
    )

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
