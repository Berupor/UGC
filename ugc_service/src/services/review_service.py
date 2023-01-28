from .base_mongo_service import BaseMongoService


class ReviewService(BaseMongoService):

    pass



def get_review_service() -> ReviewService:
    return ReviewService("movies", "reviews")
