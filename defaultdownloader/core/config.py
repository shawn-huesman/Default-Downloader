import json
import os

CONFIG_FILE_LOCATION = os.path.join(os.getcwd(), "defaultdownloader", "config", "config.json")


def get_data_path():
    return _get_file_location("data")


def get_linklist_path():
    return _get_file_location("linklist")


def get_log_path():
    return _get_file_location("logs")


def get_min_space_allowed():
    return _get_download_setting("minimum_diskspace_allowed_left_in_gb")


def _get_file_location(filename):
    with open(CONFIG_FILE_LOCATION, 'r') as file:
        config = json.load(file)
        file_path = config['file-locations'][filename]
    return file_path


def _get_download_setting(setting_name):
    with open(CONFIG_FILE_LOCATION, 'r') as file:
        config = json.load(file)
        file_path = config['download-settings'][setting_name]
    return file_path
