import random
from pprint import pprint

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from api.api import get_user_games
from . import forms
from api import api
from .models import Users, Friendship, Game, UserGameStats
from .utils import record_user_summaries, record_user_friends, record_user_games_info, get_random_game_leaderboard


def index(request):
    if request.method == 'POST':
        form = forms.SteamUrlForm(request.POST)
        if form.is_valid():
            profile_url = form.cleaned_data['profile_url']
            try:
                steamid = api.get_user_steamid(profile_url)
                current_user = Users.objects.filter(steamid=steamid)

                if current_user.exists():
                    print(f"Пользователь {steamid} уже есть в базе. Перенаправляем на профиль.")
                    return redirect('user_profile', steamid=steamid)

                record_user_summaries(steamid)
                record_user_friends(steamid, current_user)

                return redirect('user_profile', steamid=steamid)

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                form.add_error(None, "Не удалось найти пользователя по этой ссылке. Убедитесь, что ссылка верна.")

    else:
        form = forms.SteamUrlForm()

    context = {
        'form': form,
    }
    return render(request, 'index.html', context)


def user_profile(request, steamid):
    user = get_object_or_404(Users, steamid=steamid)
    record_user_games_info(steamid, current_user=user)
    request.session['steamid'] = steamid

    try:
        user_summary_data = api.get_user_summaries([steamid])[0]
    except Exception as e:
        print(f"Ошибка при получении пользователя из Steam API: {e}")
        user_summary_data = None

    context = {
        'user': user,
        'user_summary': user_summary_data,
        # 'friends': friends,
    }
    return render(request, 'user_profile.html', context)
