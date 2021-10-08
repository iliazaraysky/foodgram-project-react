from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)


class IngredientInlines(admin.StackedInline):
    model = RecipeIngredient
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', )
    list_display_links = ('id', 'name', )
    list_filter = ('tags', )
    search_fields = ('name', 'author__username', 'author__email')
    inlines = (IngredientInlines, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color', )
    list_display_links = ('id', 'name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_display_links = ('id', 'name', )
    search_fields = ('name', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount', )
    list_display_links = ('id', 'ingredient', )
    search_fields = ('ingredient__name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'favorite_recipe', )
    list_display_links = ('id', 'user', )
    search_fields = (
        'user__username',
        'user__email',
        'favorite_recipe__name',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_display_links = ('id', 'user', )
    list_filter = ('user', 'recipe', )
