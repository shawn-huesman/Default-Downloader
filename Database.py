from pymongo import MongoClient


class DefaultDB(object):
    URI = "mongodb://host.docker.internal:27017/"
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(DefaultDB.URI)
        DefaultDB.DATABASE = client['defaultdownloader']

    @staticmethod
    def get_collection(collection_name):
        return DefaultDB.DATABASE[collection_name]

    @staticmethod
    def get_docs_by_date_added(collection_name):
        collection = DefaultDB.get_collection(collection_name)
        docs = collection.find(no_cursor_timeout=True).sort("date_added")
        return docs

    @staticmethod
    def linklist_insert(data):
        collection = DefaultDB.get_collection('linklist')

        if collection.count_documents({"url": data["url"]}) == 0:
            collection.insert_one(data)
            return True
        return False

    @staticmethod
    def linklist_remove(data, match_field="url"):
        collection = DefaultDB.get_collection('linklist')
        matching_docs = collection.find({match_field: data[match_field]})

        if matching_docs:
            for doc in matching_docs:
                collection.delete_one(doc)
        return False

    @staticmethod
    def youtube_insert(data):
        collection = DefaultDB.get_collection('youtube')

        if collection.count_documents({"url": data["url"]}) == 0:
            collection.insert_one(data)
            return True
        return False

    @staticmethod
    def youtube_get_videos():
        collection = DefaultDB.get_collection('youtube')

        youtube_videos = []
        for doc in collection.find({}):
            if doc["url_type"] == "youtube-video" and not doc['downloaded']:
                youtube_videos.append(doc)

        return youtube_videos
