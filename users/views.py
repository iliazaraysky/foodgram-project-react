from rest_framework import permissions, status
from rest_framework.response import Response
from users.serializers import (
    CustomUserSerializer,
    SubCreateSerializer,
    FollowSerializer
)
from users.models import Follow, UserCustom
from djoser.views import UserViewSet
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

    @action(detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def subscribe(self, request, id=None):
        data = {
            'follower': request.user.id,
            'author': id,
        }
        serializer = SubCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        Follow.objects.filter(
            follower=user,
            author=get_object_or_404(UserCustom, id=id)
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated, ))
    def subscriptions(self, request, id=None):
        user = request.user
        subsribers = user.userFollower.all()
        page = self.paginate_queryset(subsribers)
        serializer = FollowSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
