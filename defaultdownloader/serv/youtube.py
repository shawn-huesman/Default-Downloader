import yt_dlp
import os

from defaultdownloader.Database import DefaultDB

from defaultdownloader.core.helper import get_logger, get_current_date, make_dirs_if_not_exist
from defaultdownloader.core.config import get_data_path
from defaultdownloader.core.download import download_video_using_ytdlp

logger = get_logger(__name__)

supported_populate_types = ["youtube-video", "youtube-playlist", "youtube-channel"]
supported_load_types = ["youtube-video", "youtube-playlist-video", "youtube-channel-video"]


def run():
    logger.info("Running YouTube pipeline...")

    load()
    input_dict = read()
    download(input_dict)
    organize()

    logger.info("Finished YouTube pipeline.")


def load():
    for doc in DefaultDB.get_linklist_docs():
        data = populate(doc)

        for data_entry in data:
            if "url_type" in data_entry:
                url_type = data_entry["url_type"]
                if url_type in supported_load_types:
                    if url_type == "youtube-video":
                        DefaultDB.youtube_videos_insert(data_entry)

                    elif url_type == "youtube-playlist-video":
                        playlist_id = data_entry["playlist_id"]
                        DefaultDB.youtube_playlist_insert(data_entry, playlist_id)

                    DefaultDB.linklist_remove(data_entry)


def populate(doc) -> list:
    data = {}

    if "url_type" in doc:
        if doc["url_type"] in supported_populate_types:
            url = doc["url"]
            url_type = doc["url_type"]

            if url_type == "youtube-video":
                data = _get_video_data(url)

            elif url_type == "youtube-playlist":
                data = _get_playlist_data(url)

            if isinstance(data, list):
                return data
            else:
                return [data]
    return []


def read():
    input_dict = {}
    input_dict.update({'youtube_videos': DefaultDB.youtube_get_videos_to_download()})
    input_dict.update({'youtube_playlist_videos': DefaultDB.youtube_get_playlist_videos_to_download()})

    return input_dict


def download(input_dict):
    youtube_path = _get_youtube_data_path()
    youtube_video_path = os.path.join(youtube_path, "Videos")
    youtube_playlist_path = os.path.join(youtube_path, "Playlists")
    make_dirs_if_not_exist([youtube_path, youtube_video_path, youtube_playlist_path])

    for doc in input_dict['youtube_videos']:
        url = doc["url"]
        download_video_using_ytdlp(url, youtube_video_path)
        DefaultDB.youtube_update_video_as_downloaded(doc)

    for doc in input_dict["youtube_playlist_videos"]:
        playlist_id = doc["playlist_id"]
        playlist_name = doc["playlist_name"]
        playlist_path = "{} [{}]".format(playlist_name, playlist_id)
        url = doc["url"]

        playlist_video_path = os.path.join(youtube_playlist_path, playlist_path)
        make_dirs_if_not_exist([playlist_video_path])

        download_video_using_ytdlp(url, playlist_video_path)
        DefaultDB.youtube_update_playlist_video_as_downloaded(doc, playlist_id)


def organize():
    pass


def _get_playlist_data(url):
    YDL_OPTIONS = {
        'ignoreerrors': True
    }

    url_type = "youtube-playlist-video"
    data = []
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)

        if "entries" in info:
            video_list = info["entries"]

            for i, item in enumerate(video_list):
                video = info["entries"][i]

                playlist_video_url = video.get('webpage_url', None)
                title = video.get('title', None)
                uploader = video.get('uploader', None)
                playlist_name = video.get('playlist', None)
                playlist_index = video.get('playlist_index', None)
                playlist_id = video.get('playlist_id', None)

                video_data = {
                    "url": playlist_video_url,
                    "title": title,
                    "uploader": uploader,
                    "downloaded": False,
                    "date_added": get_current_date(),
                    "url_type": url_type,
                    "playlist_name": playlist_name,
                    "playlist_index": playlist_index,
                    "playlist_id": playlist_id
                }

                data.append(video_data)

    return data


def _get_video_data(url):
    YDL_OPTIONS = {
        'ignoreerrors': True
    }

    url_type = "youtube-video"
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', None)
        uploader = info.get('uploader', None)

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
