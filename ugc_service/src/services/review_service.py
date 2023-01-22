from base_mongo_service import BaseMongoService


class ReviewService(BaseMongoService):
    pass


def get_review_service(db_name, collection_name) -> BaseMongoService:
    return BaseMongoService(db_name, collection_name)
