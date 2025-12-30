import random
from django.db.models import QuerySet
from django.utils import timezone
from api import api
from api.api import get_user_games
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
        print(f"Ошибка при получении или сохранении игр основного пользователя : {e}")


# def get_random_game_leaderboard(friends: QuerySet[Users], steamid: str):
#     user_games_ids = UserGameStats.objects.filter(user_id=steamid).values_list('game_id', flat=True)
#     user_random_gameid = random.choice(user_games_ids)
#     print(user_random_gameid)
#     game_leaderboard = {}
#     for friend in friends:
#         if (friend_db := UserGameStats.objects.filter(user_id=friend.steamid, game_id=user_random_gameid)).exists():
#             print('Информация о пользователе и игре есть базе данных')
#             game_leaderboard[friend_db[0].user.personaname] = {
#                 'game_id': friend_db[0].game_id,
#                 'playtime_forever': friend_db[0].playtime_forever,
#             }
#         else:
#             game_info = get_user_games(friend.steamid, games_id=[user_random_gameid])
#             if not game_info or game_info['game_count'] < 1:
#                 print('Continue', game_info)
#                 continue
#             print('Продолжаем обрабатывать', game_info)
#             Game.objects.update_or_create(appid=game_info['games'][0]['appid'], defaults={
#                 'appid': game_info['games'][0]['appid'],
#             })
#             UserGameStats.objects.update_or_create(game_id=game_info['games'][0]['appid'], user_id=friend.steamid,
#                                                    defaults={
#                                                        'game_id': game_info['games'][0]['appid'],
#                                                        'user_id': friend.steamid,
#                                                        'playtime_forever': game_info['games'][0]['playtime_forever'],
#                                                    })
#             game_leaderboard[friend.personaname] = game_info
#     return game_leaderboard