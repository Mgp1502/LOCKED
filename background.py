import lua_extracting
import json_util
import time
import os.path
import API_connector
# this is supposed to be the background process running. Might even be a windows service, who knows
# every 10 min, go through the

SAVE_FILE = "save_file.json"


def start():
    while True:
        save_keys()
        # if the time is on resetday, dont upload
        # TODO
        time.sleep(300)  # sleep 5 min


def save_keys():
    path = json_util.load_path(SAVE_FILE)

    folder_path = os.path.join(path, "_retail_", "WTF", "Account")

    locked_out_paths = []

    for dir in os.walk(folder_path):
        if dir[0] == "SavedVariables":
            continue
        else:
            locked_out_file = os.path.join(folder_path, dir[0], "SavedVariables", "LockedOut.lua")
            if os.path.exists(locked_out_file):
                locked_out_paths.append(locked_out_file)
    # check stored player, if none then use ""
    player = json_util.load_player(SAVE_FILE)
    for locked_path in locked_out_paths:
        lua_data = lua_extracting.extract(locked_path, check_names=True)
        for key in lua_data:
            API_connector.insert_key(key, player)


if __name__ == '__main__':
    start()

