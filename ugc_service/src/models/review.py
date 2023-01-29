from models.base_mongo import BaseMongoModel


class ShortReview(BaseMongoModel):
    text: str
    movie_id: str = ""


class FullReview(ShortReview):
    likes: list
