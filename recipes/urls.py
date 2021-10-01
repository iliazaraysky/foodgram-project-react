from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import APIRecipe, APIIngredients, APITags


router = DefaultRouter()
router.register('recipes', APIRecipe, basename='recipes')
router.register('ingredients', APIIngredients, basename='ingredients')
router.register('tags', APITags, basename='tags')

app_name = 'recipe_app'

urlpatterns = [
    path('', include(router.urls)),
]
