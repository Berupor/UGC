from .base_mongo_service import BaseMongoService


class RatingService(BaseMongoService):
    pass


def get_rating_service() -> RatingService:
    return RatingService("movies", "rating")
