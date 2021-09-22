from django.db.models import fields
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.models import UserCustom, Follow
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from recipes.models import Recipe


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=UserCustom.objects.all())],
        error_messages={
            'required': 'Необходимо заполнить email',
            'max_length': 'Недопустимое число символов. Больше 254'
        },
    )
    password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True,
        error_messages={
            'required': 'Необходимо заполнить Пароль',
            'max_length': 'Недопустимое число символов. Больше 150'
        },
        style={'input_style': 'password', 'placeholder': 'Password'}
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            'required': 'Необходимо заполнить username',
            'max_length': 'Недопустимое число символов. Больше 150'
        },
    )
    first_name = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            'required': 'Необходимо заполнить Имя',
            'max_length': 'Недопустимое число символов. Больше 150'
        },
    )
    last_name = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            'required': 'Необходимо заполнить Фамилию',
            'max_length': 'Недопустимое число символов. Больше 150'
        },
    )

    class Meta:
        model = UserCustom
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        user = UserCustom.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserMeSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserDetailSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserCustom
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        print('This is request: ', request)
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(follower=request.user, author=obj).exists()


class ShowSubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowUserSubscriptionsSerializer(UserDetailSerializers):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed', 'recipes',
                  'recipes_count')
    
    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return ShowSubscriptionRecipeSerializer(recipes, many=True).data
    
    def get_recipes_count(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return queryset.count()
