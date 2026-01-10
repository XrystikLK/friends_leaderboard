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


def record_user_friends(steamid: str, current_user: Users):
    try:
        user_friends_data = api.get_user_friends(steamid)
        if not user_friends_data:
            print(f"У пользователя {current_user.personaname} нет друзей или профиль закрыт.")
            current_user.friends_last_updated = timezone.now()
            current_user.save(update_fields=['friends_last_updated'])
            return
    except Exception as e:
        print(f"Не удалось получить список друзей для {steamid} {e}")
        return

    friend_steamids = [friend_data['steamid'] for friend_data in user_friends_data]

    all_friends_summaries = []
    chunk_size = 100
    for i in range(0, len(friend_steamids), chunk_size):
        chunk = friend_steamids[i:i + chunk_size]
        try:
            summaries_chunk = api.get_user_summaries(chunk)
            all_friends_summaries.extend(summaries_chunk)
            print(f"Запрошено {len(summaries_chunk)} профилей друзей")
        except Exception as e:
            print(f"Ошибка при получении профилей для чанка {i//chunk_size + 1} {e}")
            continue

    existing_users_map = {user.steamid: user for user in Users.objects.filter(steamid__in=friend_steamids)}
    users_to_update = []
    users_to_create = []

    for friend_summary in all_friends_summaries:
        friend_id = friend_summary['steamid']
        defaults = {
            'personaname': friend_summary.get('personaname', 'N/A'),
            'avatar_url': friend_summary.get('avatarfull', ''),
        }
        if friend_id in existing_users_map:
            user_obj = existing_users_map[friend_id]
            if user_obj.personaname != defaults['personaname'] or user_obj.avatar_url != defaults['avatar_url']:
                user_obj.personaname = defaults['personaname']
                user_obj.avatar_url = defaults['avatar_url']
                users_to_update.append(user_obj)
        else:
            users_to_create.append(Users(steamid=friend_id, **defaults))

    if users_to_create:
        Users.objects.bulk_create(users_to_create)
        print(f"Создано {len(users_to_create)} новых пользователей-друзей.")
    if users_to_update:
        Users.objects.bulk_update(users_to_update, ['personaname', 'avatar_url'])
        print(f"Обновлено {len(users_to_update)} пользователей-друзей")

    Friendship.objects.filter(from_user=current_user).delete()
    friend_objects = Users.objects.filter(steamid__in=friend_steamids)

    new_friendships = [Friendship(from_user=current_user, to_user=friend_obj) for friend_obj in friend_objects]
    if new_friendships:
        Friendship.objects.bulk_create(new_friendships)
        print(f"Создано {len(new_friendships)} связей дружбы для {current_user.personaname}")

    current_user.friends_last_updated = timezone.now()
    current_user.save(update_fields=['friends_last_updated'])
    print(f"Обновление друзей для {current_user.personaname} завершено")


def record_user_games_info(steamid: str, current_user):
    try:
        games_data = api.get_user_games(steamid, include_free_games=True)
        if 'games' in games_data:
            for game_info in games_data['games']:
                game, created = Game.objects.update_or_create(
                    appid=game_info['appid'],
                    defaults={'name': game_info.get('name', 'Unknown'), 'icon_url': game_info.get('img_icon_url', ''),}
                )
                if created:
                    print(f"Добавлена новая игра в базу: {game_info.get('name')}")

                UserGameStats.objects.update_or_create(
                    user=current_user,
                    game=game,
                    defaults={'playtime_forever': int(game_info.get('playtime_forever', 0)/60)}
                )
    except Exception as e:
        print(f"Ошибка при получении или сохранении игр основного пользователя {e}")
