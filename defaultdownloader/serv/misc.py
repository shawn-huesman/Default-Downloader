import os

from defaultdownloader.Database import DefaultDB

from defaultdownloader.core.config import get_data_path
from defaultdownloader.core.download import download_video_using_ytdlp
from defaultdownloader.core.helper import get_logger, make_dirs_if_not_exist
from defaultdownloader.serv import youtube

supported_url_types = youtube.supported_load_types + youtube.supported_populate_types

logger = get_logger(__name__)


def run():
    logger.info("Running Miscellaneous pipeline...")

    load()
    input_dict = read()
    download(input_dict)

    logger.info("Finished Miscellaneous pipeline.")


def load():
    for doc in DefaultDB.get_linklist_docs():
        data = populate(doc)
        url_type = data["url_type"]
        if url_type not in supported_url_types:
            DefaultDB.misc_insert(data)
            DefaultDB.linklist_remove(data)


def populate(doc):
    data = {
        "url_type": doc["url_type"],
        "url": doc["url"],
        "downloaded": False
    }

    return data


def read():
    input_dict = {}
    input_dict.update({'misc_docs': DefaultDB.misc_get_downloads()})

    return input_dict


def download(input_dict):
    misc_path = _get_misc_data_path()
    make_dirs_if_not_exist([misc_path])

    for doc in input_dict['misc_docs']:
        url = doc["url"]
        url_type = doc["url_type"]
        download_path = os.path.join(misc_path, url_type)
        make_dirs_if_not_exist([download_path])

        download_video_using_ytdlp(url, download_path)
        DefaultDB.misc_update_doc_as_downloaded(doc)


def _get_misc_data_path():
    data_path = get_data_path()
    youtube_path = os.path.join(data_path, "Misc")

    return youtube_path
