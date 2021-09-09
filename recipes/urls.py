from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from recipes import views


router = DefaultRouter()

app_name = 'recipe'

urlpatterns = [
    path('recipes/', views.APIRecipeList.as_view()),
]
