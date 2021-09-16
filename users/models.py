from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser)


class User(AbstractBaseUser):
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
