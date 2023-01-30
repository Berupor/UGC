from typing import AsyncGenerator

from .base_mongo_service import BaseMongoService
from .rating_service import get_rating_service


class ReviewService(BaseMongoService):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name, collection_name)
        self.rating_service = get_rating_service()

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


def get_review_service() -> ReviewService:
    return ReviewService("movies", "reviews")
