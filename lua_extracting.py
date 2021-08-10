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
    saved_characters = json_util.load_chars(SAVE_FILE)
    keys = []
    characters = lua_data['Characters']
    for character_name in characters:
        values = lua_data['Characters'][character_name]

        if values["KeystoneLevel"] > 0:
            dungeon = values["Keystone"]
            diff_level = values["KeystoneLevel"]
            keys.append((character_name, dungeon, diff_level))
    return keys

def extract_highest_weekly_key():
    return 0
