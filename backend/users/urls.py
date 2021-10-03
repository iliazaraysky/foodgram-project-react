from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.CustomUserViewSet)


app_name = 'users_app'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
