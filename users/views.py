from django.contrib.auth.models import User
from rest_framework import generics, permissions
from users.serializers import RegisterSerializer


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer


# class APIFollow(generics.ListCreateAPIView):
#     serializer_class = FollowSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('=user__username', '=following__username', )
#
#     def get_queryset(self):
#         user_following = Follow.objects.filter(
#             follwing=self.request.user).all()
#         return user_following
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
