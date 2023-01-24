from .base_mongo_service import BaseMongoService


class ReviewService(BaseMongoService):

    pass

    # def __init__(self, db_name, collection_name):
    #     super.__init__(db_name, collection_name)


def get_review_service() -> ReviewService:
    return ReviewService("movies", "reviews")
