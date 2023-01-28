from models.base_mongo import BaseMongoModel


class ShortReview(BaseMongoModel):
    text: str


class FullReview(ShortReview):
    ...
