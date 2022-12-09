from pymongo import MongoClient


class DefaultDB(object):
    URI = "mongodb://db:27017/"
    DATABASE = None
    DEFAULTDOWNLOADERDB = "defaultdownloaderdb"
    YOUTUBEVIDEODB = "youtubevideodb"
    YOUTUBEPLAYLISTDB = "youtubeplaylistdb"

    @staticmethod
    def initialize(database_name):
        client = MongoClient(DefaultDB.URI)
        DefaultDB.DATABASE = client[database_name]

    @staticmethod
    def get_collection(database_name, collection_name):
        DefaultDB.initialize(database_name)
        return DefaultDB.DATABASE[collection_name]

    @staticmethod
    def get_docs_by_date_added(database_name, collection_name):
        collection = DefaultDB.get_collection(database_name, collection_name)
        docs = collection.find(no_cursor_timeout=True).sort("date_added")
        return docs

    @staticmethod
    def get_docs_to_download(db, collection, url_type=None, only_docs_not_downloaded=True):
        collection = DefaultDB.get_collection(db, collection)

        docs = []
        for doc in collection.find({}):
            if (url_type and doc["url_type"] == url_type) or url_type is None:
                if (only_docs_not_downloaded and not doc["downloaded"]) or not only_docs_not_downloaded:
                    docs.append(doc)
        return docs

    @staticmethod
    def remove(db, collection, data, match_field="url"):
        collection = DefaultDB.get_collection(db, collection)
        matching_docs = collection.find({match_field: data[match_field]})

        if matching_docs:
            for doc in matching_docs:
                collection.delete_one(doc)
                return True
        return False

    @staticmethod
    def insert(db, collection, data, match_field="url"):
        collection = DefaultDB.get_collection(db, collection)

        if collection.count_documents({match_field: data[match_field]}) == 0:
            collection.insert_one(data)
            return True
        return False

    @staticmethod
    def update_as_downloaded(db, collection, doc, upsert=False):
        collection = DefaultDB.get_collection(db, collection)

        if collection.update_one({'_id': doc['_id']}, {'$set': {'downloaded': True}}, upsert=upsert):
            return True
        return False

    @staticmethod
    def get_linklist_docs():
        return DefaultDB.get_docs_by_date_added(DefaultDB.DEFAULTDOWNLOADERDB, "linklist")

    @staticmethod
    def linklist_insert(data):
        return DefaultDB.insert(DefaultDB.DEFAULTDOWNLOADERDB, "linklist", data)

    @staticmethod
    def linklist_remove(data):
        return DefaultDB.remove(DefaultDB.DEFAULTDOWNLOADERDB, "linklist", data)

    @staticmethod
    def youtube_videos_insert(data):
        return DefaultDB.insert(DefaultDB.YOUTUBEVIDEODB, "videos", data)

    @staticmethod
    def youtube_get_videos_to_download():
        return DefaultDB.get_docs_to_download(DefaultDB.YOUTUBEVIDEODB, "videos", "youtube-video")

    @staticmethod
    def youtube_update_video_as_downloaded(doc):
        return DefaultDB.update_as_downloaded(DefaultDB.YOUTUBEVIDEODB, "videos", doc)

    @staticmethod
    def youtube_playlist_insert(data, playlist_id):
        return DefaultDB.insert(DefaultDB.YOUTUBEPLAYLISTDB, playlist_id, data)

    @staticmethod
    def youtube_get_playlist_videos_to_download():
        client = MongoClient(DefaultDB.URI)
        DefaultDB.DATABASE = client[DefaultDB.YOUTUBEPLAYLISTDB]

        docs = []
        for playlist_collection in DefaultDB.DATABASE.list_collection_names():
            docs = docs + DefaultDB.get_docs_to_download(DefaultDB.YOUTUBEPLAYLISTDB, playlist_collection,
                                                         "youtube-playlist-video")
        return docs

    @staticmethod
    def youtube_update_playlist_video_as_downloaded(doc, playlist_id):
        return DefaultDB.update_as_downloaded(DefaultDB.YOUTUBEPLAYLISTDB, playlist_id, doc)

    @staticmethod
    def misc_insert(data):
        return DefaultDB.insert(DefaultDB.DEFAULTDOWNLOADERDB, "misc", data)

    @staticmethod
    def misc_get_downloads():
        return DefaultDB.get_docs_to_download(DefaultDB.DEFAULTDOWNLOADERDB, "misc")

    @staticmethod
    def misc_update_doc_as_downloaded(doc):
        return DefaultDB.update_as_downloaded(DefaultDB.DEFAULTDOWNLOADERDB, "misc", doc)
