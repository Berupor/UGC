from typing import List

from models.rating import ReviewRating

from .base_mongo_service import BaseMongoService


class RatingService(BaseMongoService):
    async def get_review_rating(self, field, id) -> List[ReviewRating]:
        cursor = self.find({field: id})
        return [ReviewRating(**data) async for data in cursor]


def get_rating_service() -> RatingService:
    return RatingService("movies", "rating")
