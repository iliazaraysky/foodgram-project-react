from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', )
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'author', 'tags', )
    search_fields = ('name', 'author', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color', )
    list_display_links = ('id', 'name', )
    search_fields = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_display_links = ('id', 'name', )
    search_fields = ('name', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount', )
    list_display_links = ('id', 'ingredient', )
    list_filter = ('ingredient', 'recipe', )
    search_fields = ('ingredient__name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'favorite_recipe', )
    list_display_links = ('id', 'user', )
    list_filter = ('user', 'favorite_recipe', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_display_links = ('id', 'user', )
    list_filter = ('user', 'recipe', )
