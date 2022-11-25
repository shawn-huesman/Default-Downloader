import json
from urlextract import URLExtract

from Database import DefaultDB
from Core.core_helper import get_youtubedl_type
from Core.core_config import get_linklist_path


def run():
    DefaultDB.initialize()
    input_dict = clean(read())
    update(input_dict)


def read():
    input_dict = {}

    linklist_path = get_linklist_path()

    found_urls = []
    with open(linklist_path, 'r') as file:
        for line in file:
            extractor = URLExtract()
            urls = extractor.find_urls(line)
            for url in urls:
                found_urls.append(url)

    input_dict.update({"found_urls": found_urls})

    return input_dict


def clean(input_dict):
    found_urls = input_dict["found_urls"]

    input_dict.update({"url_data": []})
    for url in found_urls:
        url_type = _find_url_type(url)
        url_data = {
            "url": url,
            "url_type": url_type
        }

        input_dict["url_data"].append(url_data)

    return input_dict


def update(input_dict):
    for url_pair in input_dict["url_data"]:
        DefaultDB.linklist_insert(url_pair)


def _find_url_type(url):
    url = str.lower(url)
    if "youtube.com/watch?v=" in url:
        return "youtube-video"
    elif "youtube.com/playlist?list=" in url:
        return "youtube-playlist"
    elif "youtube.com/" in url:
        return "youtube-channel"
    else:
        return get_youtubedl_type(url)


