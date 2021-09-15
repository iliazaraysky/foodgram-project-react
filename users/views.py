from django.contrib.auth.models import User
from rest_framework import generics, permissions
from users.serializers import RegisterSerializer


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer




