from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class UserCustom(AbstractUser):
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь подписан на'
    )
    following = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автора'
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=('user', 'following'),
                                               name='Пара уникальных значений')
                       ]
        verbose_name_plural = 'Пользователи / Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
