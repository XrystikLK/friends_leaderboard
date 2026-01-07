import random

from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

import api.api as API
from main.models import UserGameStats, Users, Game


@api_view(['GET'])
def getData(request):
    return Response({'data': {'i': 25, 'p': 25}})


@api_view(['GET'])
def getMoreData(request):
    print(request.session.get('steamid'))
    return Response({'data': {'i': 80, 'p': 80}, 'user': '1'})


@api_view(['GET'])
def get_game_leaderboard(request, appid: int):
    current_user_id = request.session.get('steamid')
    current_user_game = UserGameStats.objects.select_related('user', 'game').get(user_id=current_user_id, game_id=appid)

    friends = current_user_game.user.friends.all()
    friend_ids = [friend.steamid for friend in friends]

    existing_stats = UserGameStats.objects.filter(user_id__in=friend_ids, game_id=appid).select_related('user')
    existing_stats_map = {stat.user_id: stat for stat in existing_stats}
    print(f"Найдено {len(existing_stats_map)} записей о прохождении игры друзьями в бд")

    missing_friend_ids = [fid for fid in friend_ids if fid not in existing_stats_map]
    print(f"Не хватает данных для {len(missing_friend_ids)} друзей. Запрашиваем из API")

    stats_to_create = []
    newly_fetched_data = []
    hidden_game_profiles = 0
    without_game_profiles = 0

    missing_friends_map = {friend.steamid: friend for friend in friends if friend.steamid in missing_friend_ids}

    for friend_id in missing_friend_ids:
        friend_obj = missing_friends_map[friend_id]
        try:
            game_info = API.get_user_games(friend_id, games_id=[appid], include_free_games=True)
            if not game_info:
                hidden_game_profiles += 1
                continue
            if game_info.get('game_count', 0) < 1:
                without_game_profiles += 1
                continue

            playtime = int(game_info['games'][0].get('playtime_forever', 0) / 60)

            stats_to_create.append(UserGameStats(
                user=friend_obj,
                game=current_user_game.game,
                playtime_forever=playtime
            ))
            newly_fetched_data.append({
                "user_name": friend_obj.personaname,
                "user_icon": friend_obj.avatar_url,
                "user_steamid": friend_obj.steamid,
                "game_data": {"playtime_forever": playtime}
            })

        except Exception as e:
            print(f"Ошибка при обработке друга {friend_id} из API: {e}")
            hidden_game_profiles += 1

    if stats_to_create:
        UserGameStats.objects.bulk_create(stats_to_create)
        print(f"Сохранено {len(stats_to_create)} новых записей в БД.")

    game_leaderboard = []

    for stat in existing_stats:
        game_leaderboard.append({
            "user_name": stat.user.personaname,
            "user_icon": stat.user.avatar_url,
            "user_steamid": stat.user.steamid,
            "game_data": {"playtime_forever": stat.playtime_forever}
        })

    game_leaderboard.extend(newly_fetched_data)

    game_leaderboard.append({
        "user_name": current_user_game.user.personaname,
        "user_icon": current_user_game.user.avatar_url,
        "user_steamid": current_user_game.user.steamid,
        "game_data": {"playtime_forever": current_user_game.playtime_forever}
    })

    result = {
        'game_info': {
            'appid': appid,
            'game_title': current_user_game.game.name,
            'game_icon_hash': current_user_game.game.icon_url,
            'hidden_profiles': hidden_game_profiles,
            'without_games': without_game_profiles
        },
        "leaderboard": game_leaderboard,
    }
    return Response(result)

@api_view(['GET'])
def get_user_friends(request):
    current_user = Users.objects.get(steamid=request.session.get('steamid'))
    friends = current_user.friends.all()
    friends_obj = []
    for friend in friends:
        friends_obj.append(model_to_dict(friend))
    print(friends_obj)
    return Response(friends_obj)


@api_view(['GET'])
def get_user_games(request):
    user_games = UserGameStats.objects.filter(user_id=request.session.get('steamid'))
    result = []
    for user in user_games:
        result.append({
            "appid": user.game.appid,
            "game_title": user.game.name,
            "game_icon_hash": user.game.icon_url,
        })
    return Response(result)
