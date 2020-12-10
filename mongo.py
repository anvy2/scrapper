from pymongo import MongoClient


class Mongo:
    def __init__(self, mongoURI):
        self.mongoURI = mongoURI
        self.client = MongoClient(mongoURI)

    def get_client(self):
        return self.client

    def upload(self, data, db_name, table_name):
        db = self.client['db_name']
        collection = db[table_name]
        result = collection.insert_many(documents=data, ordered=False)

    def count(self, filter):
        result = self.count_docuements(filter)
        return result
