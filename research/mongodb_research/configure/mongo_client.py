from pymongo import MongoClient
import sys

# sys.path.append('..')
from research.mongodb_research.config import settings

mongo_client = MongoClient("mongodb://root:rootpassword@localhost:27017/")
