from django.conf import settings
from django.urls import path, include

# http://127.0.0.1:8000/api/auth/token/login/

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt'))
]
