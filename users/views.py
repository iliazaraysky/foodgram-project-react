from rest_framework import generics, permissions, status
from rest_framework import serializers
from rest_framework.response import Response
from users.serializers import (RegisterSerializer,
                               ShowUserSubscriptionsSerializer)
from users.models import Follow, UserCustom
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class RegisterView(generics.ListCreateAPIView):
    queryset = UserCustom.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer


class UserSubscriptions(UserViewSet):
    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=[permissions.IsAuthenticated]
    )
    def show_subscriptions(self, request):
        obj = User.objects.filter(userFollowing__follower=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(obj, request)
        serializer = ShowUserSubscriptionsSerializer(
            result_page,
            many=True,
            context={'current_user': request.user, 'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        url_path='subscribe',
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        if request.method == 'GET':
            author = get_object_or_404(User, id=id)
            if author != request.user:
                Follow.objects.create(
                    author=author,
                    follower=request.user
                )
                serializer = ShowUserSubscriptionsSerializer(
                    author,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя'
            )
        elif request.method == 'DELETE':
            Follow.objects.get(author_id=id, follower_id=request.user.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
