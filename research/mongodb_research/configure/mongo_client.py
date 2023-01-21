from pymongo import MongoClient  # type: ignore

mongo_client: MongoClient = MongoClient("mongodb://root:rootpassword@localhost:27017/")
