from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from . import forms, api
from .models import Users, Friendship, Game, UserGameStats


def index(request):
    if request.method == 'POST':
        form = forms.SteamUrlForm(request.POST)
        if form.is_valid():
            profile_url = form.cleaned_data['profile_url']
            try:
                steamid = api.get_user_steamid(profile_url)

                if Users.objects.filter(steamid=steamid).exists():
                    print(f"Пользователь {steamid} уже есть в базе. Перенаправляем на профиль.")
                    return redirect('user_profile', steamid=steamid)

                user_summary = api.get_user_summaries([steamid])[0]
                user, created = Users.objects.update_or_create(
                    steamid=steamid,
                    defaults={
                        'personaname': user_summary.get('personaname', 'N/A'),
                        'avatar_url': user_summary.get('avatarfull', ''),
                    }
                )

                user_friends_data = api.get_user_friends(steamid)
                friend_steamids = []
                for friend_data in user_friends_data:
                    friend_id = friend_data['steamid']
                    friend_steamids.append(friend_id)

                    friend_summary_list = api.get_user_summaries([friend_id])
                    if friend_summary_list:
                        friend_summary = friend_summary_list[0]
                        Users.objects.update_or_create(
                            steamid=friend_id,
                            defaults={
                                'personaname': friend_summary.get('personaname', 'N/A'),
                                'avatar_url': friend_summary.get('avatarfull', ''),
                            }
                        )
                    print(friend_data)
                if friend_steamids:
                    Friendship.objects.filter(from_user=user).delete()
                    friend_objects = Users.objects.filter(steamid__in=friend_steamids)
                    new_friendships = []
                    for friend_obj in friend_objects:
                        new_friendships.append(
                            Friendship(from_user=user, to_user=friend_obj)
                        )
                    
                    Friendship.objects.bulk_create(new_friendships)
                    print(f"Создано {len(new_friendships)} связей для {user.personaname}")
                user.friends_last_updated = timezone.now()
                user.save(update_fields=['friends_last_updated'])
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

    try:
        games_data = api.get_user_games(steamid, include_free_games=True)
        if 'games' in games_data:
            for game_info in games_data['games']:
                game, created = Game.objects.update_or_create(
                    appid=game_info['appid'],
                    defaults={'name': game_info.get('name', 'Unknown')}
                )
                if created:
                    print(f"Добавлена новая игра в базу: {game_info.get('name')}")

                UserGameStats.objects.update_or_create(
                    user=user,
                    game=game,
                    defaults={'playtime_forever': game_info.get('playtime_forever', 0)}
                )
    except Exception as e:
        print(f"Ошибка при получении или сохранении игр основного пользователя : {e}")

    try:
        user_summary_data = api.get_user_summaries([steamid])[0]
    except Exception as e:
        print(f"Ошибка при получении пользователя из Steam API: {e}")
        user_summary_data = None

    friends = user.friends.all()
    print(friends)

    context = {
        'user': user,
        'user_summary': user_summary_data,
        'friends': friends,
    }
    return render(request, 'user_profile.html', context)
