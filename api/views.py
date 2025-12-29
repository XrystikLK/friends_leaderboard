import random

from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.api import get_user_games
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
    print(current_user)
    friends = current_user.friends.all()
    steamid = current_user.steamid
    user_games_ids = UserGameStats.objects.filter(user_id=steamid).values_list('game_id', flat=True)
    user_random_gameid = random.choice(user_games_ids)
    print(user_random_gameid)
    game_leaderboard = {}
    for friend in friends:
        if (friend_db := UserGameStats.objects.filter(user_id=friend.steamid, game_id=user_random_gameid)).exists():
            print('Информация о пользователе и игре есть базе данных')
            game_leaderboard[friend_db[0].user.personaname] = {
                'game_id': friend_db[0].game_id,
                'playtime_forever': friend_db[0].playtime_forever,
            }
        else:
            game_info = get_user_games(friend.steamid, games_id=[user_random_gameid])
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
            game_leaderboard[friend.personaname] = game_info
    return Response(game_leaderboard)

@api_view(['GET'])
def get_user_friends(request):
    current_user = Users.objects.get(steamid=request.session.get('steamid'))
    friends = current_user.friends.all()
    friends_obj = []
    for friend in friends:
        friends_obj.append(model_to_dict(friend))
    print(friends_obj)
    return Response(friends_obj)