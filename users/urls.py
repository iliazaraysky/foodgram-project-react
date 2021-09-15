from django.conf import settings
from django.urls import path, include

from users import views

# http://127.0.0.1:8000/api/auth/token/login/

app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/', views.RegisterView.as_view(), name='auth_register'),

]
