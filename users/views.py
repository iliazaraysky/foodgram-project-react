from rest_framework import generics, permissions
from users.serializers import (RegisterSerializer,
                               ShowUserSubscriptionsSerializer)
from users.models import UserCustom
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.ListCreateAPIView):
    queryset = UserCustom.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer


class UserSubscriptions(UserViewSet):
    @action(detail=False,
            methods=['GET'],
            url_path='subscriptions',
            url_name='subscriptions',
            permission_classes=[permissions.IsAuthenticated])
    def show_subscriptions(self, request):
        obj = UserCustom.objects.filter(follow__follower=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(obj, request)
        serializer = ShowUserSubscriptionsSerializer(
            result_page,
            many=True,
            context={'current_user': request.user, 'request': request}
        )
        return paginator.get_paginated_response(serializer.data)
