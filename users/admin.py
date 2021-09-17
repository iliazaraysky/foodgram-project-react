from django.contrib import admin
from users.models import Follow, UserCustom


@admin.register(Follow)
class FollowUsers(admin.ModelAdmin):
    list_display = ('follower', 'author', )


@admin.register(UserCustom)
class CustomUsers(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', )
