import json

import requests
import os
from dotenv import load_dotenv
from pprint import pprint
from typing import TypedDict, List, NotRequired


class GameInfo(TypedDict):
    appid: int
    content_descriptorids: NotRequired[List[int]]
    has_community_visible_stats: bool
    img_icon_url: str
    name: str
    playtime_forever: int



class UserGames(TypedDict):
    game_count: int
    games: List[GameInfo]

class UserSummaries(TypedDict):
    avatar: str
    avatarfull: str
    avatarhash: str
    avatarmedium: str
    commentpermission: int
    communityvisibilitystate: int
    loccountrycode: str
    locstatecode: str
    personaname: str
    personastate: str
    personastateflags: int
    primaryclanid: str
    profilestate: int
    profileurl: str
    steamid: int
    timecreated: int

class UserFriends(TypedDict):
    friend_since: int
    relationship: str
    steamid: str

load_dotenv()

API_KEY = os.getenv('STEAM_API_KEY')
# 76561198825682828
def get_user_steamid(profile_link: str) -> str:
    user_id = profile_link.split('/')[-2]
    if user_id.isdigit():
        return user_id
    else:
        url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
        response = requests.get(url, params={
            'key': API_KEY,
            'vanityurl': user_id,
        })
        return response.json()['response']['steamid']

def get_user_games(steamid: str, include_free_games: bool = False, games_id: list[int] | None = None) -> UserGames:
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    json_params  = {
        'steamid': steamid,
        'include_appinfo': True,
        'include_played_free_games': include_free_games,
    }
    if games_id:
        json_params['appids_filter'] = games_id

    response = requests.get(url, params={
        'key': API_KEY,
        'input_json': json.dumps(json_params),
    })
    return response.json()['response']

def get_user_summaries(steamid: list[str]) -> list[UserSummaries]:
    """
    Максимальная длина steamid не должна превышать 100
    """
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    response = requests.get(url, params={
        'key': API_KEY,
        'steamids': ','.join(steamid),
    })
    return response.json()['response']['players']

def get_user_friends(steamid: str) -> list[UserFriends]:
    url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
    response = requests.get(url, params={
        'key': API_KEY,
        'steamid': steamid,
    })
    return response.json()['friendslist']['friends']

