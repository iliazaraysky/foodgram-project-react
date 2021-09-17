from rest_framework import serializers
# from django.contrib.auth.models import User
from users.models import UserCustom, Follow
from rest_framework.validators import UniqueValidator


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

    def get_is_subscribed(self, author):
        follower = self.context['request'].user
        return Follow.objects.filter(
            author__id=author.id,
            follower__id=follower.id,
            ).exists()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        following = validated_data['following']

        if user == following:
            raise serializers.ValidationError(
                {'message': 'Невозможно подписаться на самого себя'}
            )

