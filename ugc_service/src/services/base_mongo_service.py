from pymongo import MongoClient
from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient


class BaseMongoService:
    def __init__(
        self,
        db_name,
        collection_name,
        host=settings.mongo.host,
        port=settings.mongo.port,
        username=settings.mongo.username,
        password=settings.mongo.password,
    ):
        # self.client = AsyncIOMotorClient("mongodb://root:rootpassword@localhost:27017/")
        # self.db = self.client[db_name]
        # self.collection = self.db[collection_name]
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = AsyncIOMotorClient(
            f"mongodb://{username}:{password}@{host}:{port}/"
        )
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def insert_one(self, document):
        """Insert a single document into the collection"""
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def insert_many(self, documents):
        """Insert multiple documents into the collection"""
        result = await self.collection.insert_many(documents)
        return result.inserted_ids

    async def find_one(self, query):
        """Find a single document that matches the query"""
        document = await self.collection.find_one(query)
        return document

    async def find(self, query):
        """Find all documents that match the query"""
        cursor = self.collection.find(query)
        documents = []
        async for document in cursor:
            documents.append(document)
        return documents

    async def update_one(self, query, update):
        """Update a single document that matches the query"""
        result = await self.collection.update_one(query, update)
        return result.modified_count

    async def update_many(self, query, update):
        """Update all documents that match the query"""
        result = await self.collection.update_many(query, update)
        return result.modified_count

    async def delete_one(self, query):
        """Delete a single document that matches the query"""
        result = await self.collection.delete_one(query)
        return result.deleted_count

    async def delete_many(self, query):
        """Delete all documents that match the query"""
        result = await self.collection.delete_many(query)
        return result.deleted_count

    async def close(self):
        """Close the MongoDB connection"""
        await self.client.close()