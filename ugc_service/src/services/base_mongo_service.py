import pymongo


class BaseMongoService:

    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, document):
        self.collection.insert_one(document)
        print("Document created successfully.")

    def read(self, query={}):
        return self.collection.find(query)

    def update(self, query, new_values):
        self.collection.update_many(query, {"$set": new_values})
        print("Documents updated successfully.")

    def delete(self, query={}):
        self.collection.delete_many(query)
        print("Documents deleted successfully.")

    def close(self):
        self.client.close()

