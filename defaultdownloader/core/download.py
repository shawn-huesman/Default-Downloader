import shutil
import subprocess

from defaultdownloader.core.config import get_min_space_allowed
from defaultdownloader.core.helper import get_logger

logger = get_logger(__name__)


def download_video_using_ytdlp(link, download_folder, name=None):
    if is_space_available(get_min_space_allowed(), download_folder):
        if name:
            subprocess.run(["yt-dlp", link, "-o", name], cwd=download_folder)
        else:
            subprocess.run(["yt-dlp", link], cwd=download_folder)
            subprocess.run(["dpkg", "-L", "yt-dlp"], cwd=download_folder)
    else:
        logger.ERROR(
            "Less than " + str(get_min_space_allowed()) + " GB space available, will not download: " + str(link))


def space_available_in_gb(path):
    total, used, free = shutil.disk_usage(path)

    free_in_GB = (free // (2 ** 30))
    return free_in_GB


def is_space_available(space_in_gb, path):
    free_in_GB = space_available_in_gb(path)

    if int(free_in_GB) < space_in_gb:
        return False

    return True
