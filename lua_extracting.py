from slpp import slpp as lua
import json_util

SAVE_FILE = "save_file.json"

def extract(path="LockedOutTest.lua", server="Twisting Nether", max_lvl=120, check_names=False):
    """

    :param path: path to lockedOut datafile, found under WTF,
    :param server: which server to look at
    :param max_lvl: the current max lvl of the expansion
    :return: List of tuples containing (char_name, instance, key_level)

    """
    f = open(path, "r", encoding="utf-8")
    next(f)  # skip first line
    code = f.read()
    # ignore first 12 chars to remove the "LockoutDb = "
    code = code[12:]

    # decode the lua.
    lua_data = lua.decode(code)

    char_data = json_util.load_chars(SAVE_FILE)
    print()
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
