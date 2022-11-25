import json


def get_linklist_path():
    return _get_file_location("linklist")


def _get_file_location(filename):
    with open("./User/config.json", 'r') as file:
        config = json.load(file)
        file_path = config['file-locations'][filename]
    return file_path
