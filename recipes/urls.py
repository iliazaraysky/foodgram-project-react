from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from recipes import views


router = DefaultRouter()

app_name = 'recipe'

urlpatterns = [
    path('recipes/', views.APIRecipeList.as_view()),
    path('recipes/<int:pk>/', views.APIRecipeDetail.as_view(),
         name='api_recipe_detail'),
    path('tags/', views.APITagList.as_view()),
    path('tags/<int:pk>/', views.APITagDetail.as_view()),
    path('ingredients/<int:pk>/', views.APIIngredientsDetail.as_view()),
    path('ingredients/', views.APIIngredientsList.as_view()),
]
