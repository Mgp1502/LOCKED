import json
import os.path
import API_connector


def load_save_file_as_json(filename):
    # load saved data from 'filename'
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            return data
    else:
        return {}


def save_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def save_file_exist_with_path(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            if 'path' in data.keys():
                if data['path'] is not "":
                    return True
    return False


def load_tracked_characters(filename):
    data = load_save_file_as_json(filename)
    if 'chars' in data.keys():
        return data['chars'] or []
    else:
        return []


def load_path(filename):
    data = load_save_file_as_json(filename)
    if 'path' in data.keys():
        return data['path'] or ""
    else:
        return ""


def load_player(filename):
    # check stored player, if none then use ""
    data = load_save_file_as_json(filename)
    if 'player' in data.keys():
        return data['player'] or ""
    else:
        return ""


def save_path(path, filename):
    # saves the given path in the json file 'filename'
    data = load_save_file_as_json(filename)
    data['path'] = path
    save_json(data, filename)


def save_player(player, filename):
    data = load_save_file_as_json(filename)
    data['player'] = player
    save_json(data, filename)


def save_chars(char_names, filename):
    # delete the now "not tracked" chars from the DB
    old_chars = set(load_tracked_characters(filename))
    new_chars = set(char_names)
    chars_to_delete = old_chars.difference(new_chars)

    if chars_to_delete:
        for char in chars_to_delete:
            API_connector.delete_key_by_char_name(char)

    # add the new tracked chars to the save file.
    data = load_save_file_as_json(filename)
    data['chars'] = char_names
    save_json(data, filename)
    return chars_to_delete
