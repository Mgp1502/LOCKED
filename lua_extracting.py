from slpp import slpp as lua
import json_util

SAVE_FILE = "save_file.json"


def getLuaObject(path):
    f = open(path, "r", encoding="utf-8")
    next(f)  # skip first line
    code = f.read()
    # ignore the chars untill first '{' is encountered
    code = code[code.find('{'):]
    return lua.decode(code)


def extractkeys(path, check_names=False):
    """
    Extracts keys information from a LUA datafile
    :param path: path to datafile, found under WTF
    :return: List of tuples containing (char_name, instance, key_level)

    """
    lua_data = getLuaObject(path)
    tracked_characters = json_util.load_tracked_characters(SAVE_FILE)
    keys = []
    characters = []
    try:
        characters = lua_data['Characters']
    except KeyError:
        print("no characters found in -> " + path)
    for character_name in characters:
        if check_names:
            if character_name not in tracked_characters:
                continue

        values = lua_data['Characters'][character_name]

        if values["KeystoneLevel"] > 0:
            dungeon = values["Keystone"]
            diff_level = values["KeystoneLevel"]
            keys.append((character_name, dungeon, diff_level))
    return keys

def extract_highest_weekly_key():
    return 0
