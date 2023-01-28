from pydantic import Field

from models.base_mongo import BaseMongoModel


class Rating(BaseMongoModel):
    rating: int = Field(default=0, ge=0, le=10)


class MovieRating(Rating):
    movie_id: str = None


class ReviewRating(Rating):
    review_id: str = None
