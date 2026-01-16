from django.contrib import admin
from .models import Users, Friendship, Game, UserGameStats

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('personaname', 'steamid', 'friends_last_updated')
    search_fields = ('personaname', 'steamid')
    readonly_fields = ('friends_last_updated',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'appid')
    search_fields = ('name', 'appid')

@admin.register(UserGameStats)
class UserGameStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'playtime_forever')
    list_filter = ('game',)
    search_fields = ('user__personaname', 'game__name')
    ordering = ('-playtime_forever',)

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    search_fields = ('from_user__personaname', 'to_user__personaname')