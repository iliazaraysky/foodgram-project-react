from django.contrib import admin
from users.models import Follow, UserCustom


@admin.register(Follow)
class FollowUsers(admin.ModelAdmin):
    list_display = ('id', 'follower', 'author', )
    list_display_links = ('id', 'follower', )
    list_filter = ('follower', 'author', )


@admin.register(UserCustom)
class CustomUsers(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', )
    list_display_links = ('id', 'username', 'first_name', 'last_name', )
    search_fields = ('username', )
