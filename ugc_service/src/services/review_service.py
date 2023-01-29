from typing import AsyncGenerator

from fastapi import Depends

from .base_mongo_service import BaseMongoService
from .rating_service import RatingService, get_rating_service


class ReviewService(BaseMongoService):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name, collection_name)
        self.rating_service = get_rating_service()

    async def find(self, query):
        """Find all documents that match the query"""
        pipeline = [
            {"$match": {**query}},
            {
                "$lookup": {
                    "from": "rating",
                    "localField": "_id",
                    "foreignField": "review_id",
                    "as": "likes",
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "created_at": {"$first": "$created_at"},
                    "user_id": {"$first": "$user_id"},
                    "text": {"$first": "$text"},
                    "movie_id": {"$first": "$movie_id"},
                    "likes": {"$sum": {"$size": "$likes"}}
                }
            },
            {
                "$sort": {
                    "likes": -1
                }}
        ]

        cursor = self.collection.aggregate(pipeline)
        async for document in cursor:
            yield document


def get_review_service() -> ReviewService:
    return ReviewService("movies", "reviews")
