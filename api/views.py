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
    current_user = Users.objects.get(steamid=request.session.get('steamid'))
    friends = current_user.friends.all()
    steamid = current_user.steamid
    # user_games_ids = UserGameStats.objects.filter(user_id=steamid).values_list('game_id', flat=True)
    # user_random_gameid = random.choice(user_games_ids)
    # print(user_random_gameid)
    game_leaderboard = []
    for friend in friends:
        if (friend_db := UserGameStats.objects.filter(user_id=friend.steamid, game_id=appid)).exists():
            print('Информация о пользователе и игре есть базе данных')
            game_data = {
                'playtime_forever': friend_db[0].playtime_forever,
            }
            game_leaderboard.append({"user_name": friend_db[0].user.personaname, "game_data": game_data})
        else:
            game_info = API.get_user_games(friend.steamid, games_id=[appid])
            if not game_info or game_info['game_count'] < 1:
                print('Continue', game_info)
                continue
            print('Продолжаем обрабатывать', game_info)
            Game.objects.update_or_create(appid=game_info['games'][0]['appid'], defaults={
                'appid': game_info['games'][0]['appid'],
            })
            UserGameStats.objects.update_or_create(game_id=game_info['games'][0]['appid'], user_id=friend.steamid,
                                                   defaults={
                                                       'game_id': game_info['games'][0]['appid'],
                                                       'user_id': friend.steamid,
                                                       'playtime_forever': game_info['games'][0]['playtime_forever'],
                                                   })
            game_leaderboard.append({"user_name": friend.personaname, "game_data": {
                'playtime_forever': int(game_info['games'][0]['playtime_forever']/60),
            }})

            # if 'game_info' not in result:
            #     result['game_info'] = {
            #         "game_id": game_info['games'][0]['appid'],
            #         "playtime_forever": game_info['games'][0]['playtime_forever'],
            #         "image_url": game_info['games'][0]['img_icon_url'],
            #         "game_title": game_info['games'][0]['name'],
            #     }
            #     print('1 Раз заполнили')
    game_info = Game.objects.get(appid=appid)

    result = {
        'game_info': {
            'appid': appid,
            'game_title': game_info.name,
            'game_icon_hash': game_info.icon_url,
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