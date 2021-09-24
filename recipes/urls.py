from django.db.models import base
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes import views
from recipes.views import APIRecipe


router = DefaultRouter()
router.register('recipes', APIRecipe, basename='recipes')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', views.APITagList.as_view()),
    path('tags/<int:pk>/', views.APITagDetail.as_view()),
    path('ingredients/<int:pk>/', views.APIIngredientsDetail.as_view()),
    path('ingredients/', views.APIIngredientsList.as_view()),
    
]
