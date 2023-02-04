from typing import AsyncGenerator

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .base_mongo_service import BaseMongoService, get_database_conn


class ReviewService(BaseMongoService):
    def __init__(self, db_name, collection_name, database_conn):
        super().__init__(db_name, collection_name, database_conn)
        self.rating_service = database_conn

    async def find(self, query, sort_field="", order="") -> AsyncGenerator:
        """Find all documents that match the query"""
        pipeline = [
            {"$match": {**query}},
            {
                "$lookup": {
                    "from": "rating",
                    "localField": "_id",
                    "foreignField": "review_id",
                    "as": "rating",
                }
            },
            {
                "$addFields": {
                    "likes": {
                        "$filter": {
                            "input": "$rating",
                            "as": "rating",
                            "cond": {"$eq": ["$$rating.rating", 10]},
                        }
                    },
                    "dislikes": {
                        "$filter": {
                            "input": "$rating",
                            "as": "rating",
                            "cond": {"$eq": ["$$rating.rating", 0]},
                        }
                    },
                }
            },
            {
                "$addFields": {
                    "likes": {"$size": "$likes"},
                    "dislikes": {"$size": "$dislikes"},
                }
            },
            {"$sort": {sort_field: order}},
        ]

        cursor = self.collection.aggregate(pipeline)
        async for document in cursor:
            yield document


def get_review_service(
    database_conn: AsyncIOMotorClient = Depends(get_database_conn),
) -> ReviewService:
    return ReviewService("movies", "reviews", database_conn)
