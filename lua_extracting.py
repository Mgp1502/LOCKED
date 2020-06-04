from slpp import slpp as lua
import json_util

SAVE_FILE = "save_file.json"

def getLuaObject(path):
    f = open(path, "r", encoding="utf-8")
    next(f)  # skip first line
    code = f.read()
    # ignore first 12 chars to remove the "LockoutDb = "
    code = code[12:]

    # decode the lua.
    return lua.decode(code)


def extractkeys(path="LockedOutTest.lua", server="Twisting Nether", max_lvl=120, check_names=False):
    """

    :param path: path to lockedOut datafile, found under WTF,
    :param server: which server to look at
    :param max_lvl: the current max lvl of the expansion
    :return: List of tuples containing (char_name, instance, key_level)

    """
    lua_data = getLuaObject(path)
    char_data = json_util.load_chars(SAVE_FILE)
    keys = []
    for character in lua_data[server]:
        if character["currentLevel"] == max_lvl and (not check_names or (character["charName"] in char_data)):
            for instance in character["instances"]:
                dungeon = character["instances"][instance]
                if "keystone" in dungeon:
                    diff_level = dungeon["keystone"]["difficulty"]
                    # print(character["charName"] + ": " + instance + " +" + str(diff_level))
                    keys.append((character["charName"], instance, diff_level))
                    break
    return keys


def extract_highest_weekly_key(char_name, path="LockedOutTest.lua", server="Twisting Nether"):
    lua_data = getLuaObject(path)
    highest_key = 0

    for character in lua_data[server]:
        if character["charName"] == char_name:
            for instance in character["instances"]:
                dungeon = character["instances"][instance]
                if "mythicbest" in dungeon:
                    diff_level = dungeon["mythicbest"]["difficulty"]
                    if diff_level > highest_key:
                        highest_key = diff_level

    return highest_key





