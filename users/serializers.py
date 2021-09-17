from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
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
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        user = User.objects.create(
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
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', )


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field='username',
#         default=serializers.CurrentUserDefault(),
#         read_only=True
#     )
#     following = serializers.SlugRelatedField(
#         read_only=False,
#         queryset=User.objects.all(),
#         slug_field='username'
#     )
#
#     class Meta:
#         fields = ('user', 'following')
#         model = Follow
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following')
#             )
#         ]
#
#     def validate_following(self, following):
#         if self.context.get('request').method == 'POST':
#             if self.context.get('request').user == following:
#                 raise serializers.ValidationError(
#                     'Вы не можете подписаться на самого себя'
#                 )
#         return following
