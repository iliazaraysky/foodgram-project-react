from django.contrib import admin
from users.models import Follow


@admin.register(Follow)
class FollowUsers(admin.ModelAdmin):
    list_display = ('user', 'following', )
