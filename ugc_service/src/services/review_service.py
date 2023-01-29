from typing import AsyncGenerator

from fastapi import Depends

from .base_mongo_service import BaseMongoService
from .rating_service import RatingService, get_rating_service


class ReviewService(BaseMongoService):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name, collection_name)
        self.rating_service = get_rating_service()

    async def find(self, query, sort=None) -> AsyncGenerator:
        """Find all documents that match the query"""
        cursor = self.collection.find(query).sort(sort, 1)
        async for document in cursor:
            document["likes"] = await self.rating_service.get_review_rating(
                "review_id", document["_id"]
            )
            yield document


def get_review_service() -> ReviewService:
    return ReviewService("movies", "reviews")
