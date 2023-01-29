from pydantic import Field, Extra
from bson import ObjectId
from models.base_mongo import BaseMongoModel, PyObjectId


class Rating(BaseMongoModel):
    rating: int = Field(default=0, ge=0, le=10)


class MovieRating(Rating):
    movie_id: str = ''


class ReviewRating(Rating):
    review_id: PyObjectId = None
