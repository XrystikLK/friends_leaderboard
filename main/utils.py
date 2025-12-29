from django.utils import timezone
from api import api
from main.models import Users, Friendship, Game, UserGameStats


def record_user_summaries(steamid: str):
    user_summary = api.get_user_summaries([steamid])[0]
    user, created = Users.objects.update_or_create(
        steamid=steamid,
        defaults={
            'personaname': user_summary.get('personaname', 'N/A'),
            'avatar_url': user_summary.get('avatarfull', ''),
        }
    )

def record_user_friends(steamid: str, current_user):
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
        Friendship.objects.filter(from_user=current_user[0]).delete()
        friend_objects = Users.objects.filter(steamid__in=friend_steamids)
        new_friendships = []
        for friend_obj in friend_objects:
            new_friendships.append(
                Friendship(from_user=current_user[0], to_user=friend_obj)
            )

        Friendship.objects.bulk_create(new_friendships)
        print(f"Создано {len(new_friendships)} связей для {current_user[0].personaname}")
    current_user[0].friends_last_updated = timezone.now()
    current_user[0].save(update_fields=['friends_last_updated'])

def record_user_games_info(steamid: str, current_user):
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
                    user=current_user,
                    game=game,
                    defaults={'playtime_forever': game_info.get('playtime_forever', 0)}
                )
    except Exception as e:
        print(f"Ошибка при получении или сохранении игр основного пользователя : {e}")