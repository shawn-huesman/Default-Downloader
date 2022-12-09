from urlextract import URLExtract

from defaultdownloader.Database import DefaultDB
from defaultdownloader.core.helper import get_ytdlp_type
from defaultdownloader.core.config import get_linklist_path

from defaultdownloader.core.helper import get_logger

logger = get_logger(__name__)


def run():
    logger.info("Running serv linklist pipeline...")

    input_dict = clean(read())
    update(input_dict)
    clear_linklist()

    logger.info("Finished serv linklist pipeline.")


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

    logger.info("Found " + str(len(found_urls)) + " urls in linklist.")
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
    urls_inserted = 0
    for url_pair in input_dict["url_data"]:
        if DefaultDB.linklist_insert(url_pair):
            urls_inserted = urls_inserted + 1

    logger.info("Inserted " + str(urls_inserted) + " urls into linklist collection.")


def clear_linklist():
    f = open(get_linklist_path(), 'w+')
    f.truncate(0)


def _find_url_type(url):
    url = str.lower(url)
    if "youtube.com/playlist?list=" in url or ("youtube.com" in url and "&list=" in url):
        return "youtube-playlist"
    elif "youtube.com/watch?v=" in url:
        return "youtube-video"
    elif "youtube.com/" in url:
        return "youtube-channel"
    else:
        return get_ytdlp_type(url)
