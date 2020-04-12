import json
import os.path


def load_json(filename):
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


def load_chars(filename):
    data = load_json(filename)
    if 'chars' in data.keys():
        return data['chars'] or []
    else:
        return []


def load_path(filename):
    data = load_json(filename)
    if 'path' in data.keys():
        return data['path'] or ""
    else:
        return ""

def save_path(path, filename):
    # saves the given path in the json file 'filename'
    data = load_json(filename)
    data['path'] = path
    save_json(data, filename)


def save_chars(char_names, filename):
    # add the char to the saved data file, if already exist dont.
    data = load_json(filename)
    data['chars'] = char_names
    save_json(data, filename)
