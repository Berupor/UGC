from bson import ObjectId
from models.base_mongo import BaseMongoModel, PyObjectId
from pydantic import Extra, Field


class Rating(BaseMongoModel):
    rating: int = Field(default=0, ge=0, le=10)
    source_id: str = Field(default="")
    type: str = Field(default="movie")


#
# class MovieRating(Rating):
#     movie_id: str = ""
#
#
# class ReviewRating(Rating):
#     review_id: PyObjectId = None  # type: ignore
