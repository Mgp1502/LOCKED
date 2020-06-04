import requests
import lua_extracting


def insert_key(key, player):
    (name, dungeon, level) = key
    payload = {'name': name, 'dungeon': dungeon, 'level': level, 'player': player}
    url = 'https://www.alpha-brawl.com/api/keys?code=coolhoot123'
    header = {"User-Agent": "XY", "charset": "utf-8"}
    r = requests.post(url=url, data=payload, headers=header)
    print(r)


def delete_key_by_char_name(name):
    url = 'https://www.alpha-brawl.com/api/keys?name=' + name
    header = {"User-Agent": "XY", "charset": "utf-8"}
    r = requests.delete(url=url, headers=header)
    print(r)