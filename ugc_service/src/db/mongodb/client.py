from pymongo import MongoClient

client = MongoClient("mongodb+srv://eugene:iEW7kga69Y5qJucW@cluster0.t2rby2w.mongodb.net/?retryWrites=true&w=majority")

db = client.test
