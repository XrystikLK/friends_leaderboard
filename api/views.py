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
    current_user_game = UserGameStats.objects.get(user_id=request.session.get('steamid'), game_id=appid)
    friends = current_user_game.user.friends.all()
    # user_games_ids = UserGameStats.objects.filter(user_id=steamid).values_list('game_id', flat=True)
    # user_random_gameid = random.choice(user_games_ids)
    # print(user_random_gameid)
    game_leaderboard = []
    hidden_game_profiles = 0
    without_game_profiles = 0
    for friend in friends:
        if (friend_db := UserGameStats.objects.filter(user_id=friend.steamid, game_id=appid)).exists():
            print('Информация о пользователе и игре есть базе данных')
            game_data = {
                'playtime_forever': friend_db[0].playtime_forever,
            }
            game_leaderboard.append(
                {"user_name": friend_db[0].user.personaname, 'user_icon': friend_db[0].user.avatar_url,
                 'user_steamid': friend_db[0].user.steamid, "game_data": game_data})
        else:
            game_info = API.get_user_games(friend.steamid, games_id=[appid], include_free_games=True)
            if not game_info or game_info['game_count'] < 1:
                if not game_info:
                    hidden_game_profiles += 1
                else:
                    without_game_profiles += 1
                print('Continue', game_info, friend.steamid, friend.personaname, appid, hidden_game_profiles, without_game_profiles)
                continue
            print('Продолжаем обрабатывать', game_info)
            Game.objects.update_or_create(appid=game_info['games'][0]['appid'], defaults={
                'appid': game_info['games'][0]['appid'],
            })
            UserGameStats.objects.update_or_create(game_id=game_info['games'][0]['appid'], user_id=friend.steamid,
                                                   defaults={
                                                       'game_id': game_info['games'][0]['appid'],
                                                       'user_id': friend.steamid,
                                                       'playtime_forever': int(game_info['games'][0]['playtime_forever'] / 60),
                                                   })
            game_leaderboard.append({"user_name": friend.personaname, 'user_icon': friend.avatar_url,
                                     'user_steamid': friend.steamid, "game_data": {
                    'playtime_forever': int(game_info['games'][0]['playtime_forever'] / 60),
                }})

            # if 'game_info' not in result:
            #     result['game_info'] = {
            #         "game_id": game_info['games'][0]['appid'],
            #         "playtime_forever": game_info['games'][0]['playtime_forever'],
            #         "image_url": game_info['games'][0]['img_icon_url'],
            #         "game_title": game_info['games'][0]['name'],
            #     }
            #     print('1 Раз заполнили')

    game_leaderboard.append({
        "user_name": current_user_game.user.personaname,
        "user_icon": current_user_game.user.avatar_url,
        "user_steamid": current_user_game.user.steamid,
        "game_data": {
            "playtime_forever": current_user_game.playtime_forever,
        }})

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
