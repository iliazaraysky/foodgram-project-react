# from django.contrib.auth.models import User
from rest_framework import generics, permissions
from djoser.serializers import UserSerializer
from djoser.views import UserViewSet
from users.serializers import RegisterSerializer
from users.models import UserCustom, Follow


class RegisterView(generics.ListCreateAPIView):
    queryset = UserCustom.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer

