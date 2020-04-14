from lua_extracting import extract
import json_util
import time
import os.path
import requests
# this is supposed to be the background process running. Might even be a windows service, who knows
# every 10 min, go through the

SAVE_FILE = "save_file.json"

def start():
    while True:
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

        for locked_path in locked_out_paths:
            lua_data = extract(locked_path, check_names=True)
            for key in lua_data:
                insert_key(key)
        time.sleep(300)  # sleep 5 min


def insert_key(key):
    (name, dungeon, level) = key
    payload = {'name': name, 'dungeon': dungeon, 'level': level}
    url = 'https://www.alpha-brawl.com/api/insertkey'
    #header = {'Content-type': 'application/json', "User-Agent": "XY"}
    header = {"User-Agent": "XY"}
    r = requests.post(url=url, data=payload, headers=header)

    print(r)


if __name__ == '__main__':
    start()

