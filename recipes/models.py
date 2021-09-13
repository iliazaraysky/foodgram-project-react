from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        unique=True,
        verbose_name='Название тега',
        help_text='Укажите название тега'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        verbose_name='Цвет',
        help_text='Цветовой HEX-код. 6 символов'
    )
    slug = models.SlugField(
        max_length=200,
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
    name = models.CharField(
        max_length=120,
        verbose_name='Название ингредиента',
        help_text='Укажите название игредиента',
        unique=True,
        null=True
    )

    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Единицы измерения',
        help_text='Укажите единицу измерения',
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Ингридиент'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        help_text='Обязательно укажите ингредиенты',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Ваш рецепт будет намного проще найти, если добавить тег'
    )

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='recipes_photo',
        verbose_name='Фотография',
        help_text='Рецепты в с фото чаще попадают в избранное'
    )

    name = models.CharField(
        max_length=180,
        null=False,
        blank=False,
        verbose_name='Название рецепта',
        help_text='У блюда должно быть название'
    )

    text = models.TextField(
        null=True,
        blank=False,
        verbose_name='Описание',
        help_text='Обязательно добавьте описание'
    )

    cooking_time = models.PositiveIntegerField(
        null=True,
        blank=False,
        default=1,
        verbose_name='Время приготовления в минутах',
        help_text='Время приготовления не может быть равным 0'
    )

    class Meta:
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_for_recipe',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_for_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    amount = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Количество',
        help_text='Укажите количество'
    )

    class Meta:
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return f'{self.recipe} : {self.ingredient}'
