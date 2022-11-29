import yt_dlp
import os

from Database import DefaultDB

from Core.core_helper import get_logger, get_current_date, make_dirs_if_not_exist
from Core.core_config import get_data_path
from Core.core_download import download_video_using_ytdlp

logger = get_logger(__name__)


def run():
    logger.info("Running YouTube pipeline...")

    DefaultDB.initialize()
    load()
    input_dict = read()
    update(input_dict)
    download(input_dict)
    organize()

    logger.info("Finished YouTube pipeline.")


def load():
    for doc in DefaultDB.get_docs_by_date_added("linklist"):
        data = populate(doc)

        for data_entry in data:
            DefaultDB.youtube_insert(data_entry)
            DefaultDB.linklist_remove(data_entry)


def read():
    input_dict = {}
    input_dict.update({'youtube_videos': DefaultDB.youtube_get_videos()})

    return input_dict


def clean():
    pass


def update(input_dict):
    pass


def download(input_dict):
    youtube_path = _get_youtube_data_path()
    youtube_video_path = os.path.join(youtube_path, "Videos")
    make_dirs_if_not_exist([youtube_path, youtube_video_path])

    for doc in input_dict['youtube_videos']:
        url = doc["url"]
        download_video_using_ytdlp(url, youtube_video_path)
        doc["downloaded"] = True


def organize():
    pass


def populate(doc) -> list:
    supported_types = ["youtube-video", "youtube-playlist", "youtube-channel"]
    data = {}

    if "url_type" in doc:
        if doc["url_type"] in supported_types:
            url = doc["url"]
            url_type = doc["url_type"]

            if url_type == "youtube-video":
                data = _get_video_data(url)

    if isinstance(data, list):
        return data
    else:
        return [data]


def _get_video_data(url):
    YDL_OPTIONS = {
        'ignoreerrors': True
    }

    url_type = "youtube-video"
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
        uploader = info_dict.get('uploader', None)

        data = {
            "url": url,
            "title": title,
            "uploader": uploader,
            "downloaded": False,
            "date_added": get_current_date(),
            "url_type": url_type
        }

    return data


def _get_youtube_data_path():
    data_path = get_data_path()
    youtube_path = os.path.join(data_path, "Youtube")

    return youtube_path
