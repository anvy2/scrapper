from pymongo import MongoClient


class Mongo:
    def __init__(self, mongoURI):
        self.mongoURI = mongoURI
        self.client = MongoClient(mongoURI)

    def get_client(self):
        return self.client

    def upload(self, data):
        db = self.client['db']
        collection = db['articles']
        result = collection.insert_many(documents=data, ordered=False)
