import yt_dlp.extractor
import logging
import datetime
import os
from sys import stdout

from defaultdownloader.core.config import get_log_path


def get_ytdlp_type(url):
    extractors = yt_dlp.extractor.gen_extractors()

    extractor_name = None
    for extractor in extractors:
        if extractor.suitable(url) and extractor.IE_NAME != 'generic':
            extractor_name = str(extractor).split('.')[-1].split(' ')[0]

    return extractor_name


def get_logger(name):
    log_format = "%(asctime)s [%(process)s] [%(threadName)-12.12s] [%(levelname)-5.5s] " \
                 "[%(pathname)s] [%(funcName)s:%(lineno)d] \n %(message)s \n"
    log_formatter = logging.Formatter(log_format)

    root_logger = logging.getLogger(name)
    root_logger.setLevel(logging.DEBUG)
    root_logger.propagate = False

    log_path = get_log_path()
    file_name = timestamp_filename("ddlog")
    file_handler_path = os.path.join(log_path, timestamp_ymd())
    make_dirs_if_not_exist([file_handler_path])
    file_handler_filepath = os.path.join(file_handler_path, file_name + ".log")

    file_handler = logging.FileHandler(file_handler_filepath)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(log_formatter)
    root_logger.addHandler(consoleHandler)

    return root_logger


def make_dirs_if_not_exist(list_of_dirs):
    if not isinstance(list_of_dirs, list):
        list_of_dirs = [list_of_dirs]

    for directory in list_of_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)


def timestamp_filename(filename):
    format = "%Y-%m-%d %H.%M.%S {fname}".format(fname=filename)
    return datetime.datetime.now().strftime(format)


def timestamp_ymd():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_current_date():
    return datetime.datetime.today().replace(microsecond=0)
