from django.contrib import admin
from django.urls import path, include

import api.views
import main.views
from friends_leaderboard import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index, name='index'),
    path('user/<str:steamid>/', main.views.user_profile, name='user_profile'),
    path('api/leaderboard/<int:appid>/', api.views.get_game_leaderboard),

    path('api/friends/', api.views.get_user_friends),
    path('api/games/', api.views.get_user_games),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

