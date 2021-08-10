import datetime

import lua_extracting
import json_util
import time
import os.path
import API_connector
# this is the background process running.
# every 5 min, look for the lua files and upload some data
# on reset day delete the lua files

SAVE_FILE = "save_file.json"


def start():
    while True:

        # if the time is on resetday, dont upload
        # TODO
        reset = check_if_need_of_reset()
        if not reset:
            save_keys()
        time.sleep(300)  # sleep 5 min


def check_if_need_of_reset():
    now = datetime.datetime.utcnow()
    two_hours = datetime.timedelta(hours=2)
    now = now + two_hours
    if now.weekday() == 2 and now.hour == 8 and now.minute > 30:
        for lua_file in find_lua_files():
            os.remove(lua_file)
        return True
    return False


def save_keys():
    player = json_util.load_player(SAVE_FILE)
    for locked_path in find_lua_files():
        lua_data = lua_extracting.extractkeys(locked_path, check_names=True)
        for key in lua_data:
            highest_done = lua_extracting.extract_highest_weekly_key()
            API_connector.post_key(key, player, highest_done)


def find_lua_files():
    path = json_util.load_path(SAVE_FILE)

    folder_path = os.path.join(path, "_retail_", "WTF", "Account")
    locked_out_paths = []

    for dir in os.walk(folder_path):
        if dir[0] == "SavedVariables":
            continue
        else:
            locked_out_file = os.path.join(folder_path, dir[0], "SavedVariables", "AB_Locked.lua")
            if os.path.exists(locked_out_file):
                locked_out_paths.append(locked_out_file)
    return locked_out_paths


if __name__ == '__main__':
    start()

