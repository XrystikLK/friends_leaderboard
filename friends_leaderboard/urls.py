"""
URL configuration for friends_leaderboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('api/test', api.views.getMoreData)
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

