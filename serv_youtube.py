import youtube_dl

from Database import DefaultDB


def run():
    DefaultDB.initialize()
    load()
    input_dict = read()
    update(input_dict)
    quick_print_docs()


def load():
    for doc in DefaultDB.get_docs_by_date_added("linklist"):
        data = populate(doc)

        for data_entry in data:
            DefaultDB.youtube_insert(data_entry)
            DefaultDB.linklist_remove(data_entry)


def quick_print_docs():
    print("")
    print("--youtube--")
    for doc in DefaultDB.get_docs_by_date_added("youtube"):
        print(doc)

    print("")
    print("--linklist--")
    for doc in DefaultDB.get_docs_by_date_added("linklist"):
        print(doc)

    print("")
    print("--archive--")
    for doc in DefaultDB.get_docs_by_date_added("archive"):
        print(doc)


def populate(doc):
    supported_types = ["youtube-video", "youtube-playlist", "youtube-channel"]
    data = {}

    if "url_type" in doc:
        if doc["url_type"] in supported_types:
            url = doc["url"]
            url_type = doc["url_type"]

            if url_type == "youtube-video":
                data = _get_video_data(url)

    return data


def read():
    input_dict = {}

    return input_dict


def clean():
    pass


def update(input_dict):
    pass


def _get_video_data(url):
    YDL_OPTIONS = {
        'ignoreerrors': True
    }

    data = {}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
        uploader = info_dict.get('uploader', None)

        data.update({'url': url})
        data.update({'title': title})
        data.update({'uploader': uploader})

    return [data]
