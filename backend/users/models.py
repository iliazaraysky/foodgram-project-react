from django.db import models
from django.contrib.auth.models import AbstractUser


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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        UserCustom,
        null=True,
        on_delete=models.CASCADE,
        related_name='userFollower',
        verbose_name='Пользователь подписан на'
    )
    author = models.ForeignKey(
        UserCustom,
        null=True,
        related_name='userFollowing',
        on_delete=models.CASCADE,
        verbose_name='Автора'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'author'),
                name='unique_following'
            ),
        )
        verbose_name_plural = 'Пользователи / Подписки'

    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
