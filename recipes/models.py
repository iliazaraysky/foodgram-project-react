from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Название тега',
        help_text='Укажите название тега'
    )
    HEX_code = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        verbose_name='Цвет',
        help_text='Цветовой HEX-код. 6 символов'
    )
    slug = models.SlugField(
        max_length=45,
        unique=True,
        verbose_name='Slug (идентификатор)',
        help_text='Slug это уникальная строка, понятная человеку'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Тег'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    pass


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=180,
        null=False,
        blank=False,
        verbose_name='Название рецепта',
        help_text='У блюда должно быть название'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание',
        help_text='Обязательно добавьте описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Обязательно укажите ингредиенты',
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Ваш рецепт будет намного проще найти, если добавить тег'
    )

    class Meta:
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
