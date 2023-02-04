from models.base_mongo import BaseMongoModel
from pydantic import Field


class Rating(BaseMongoModel):
    rating: int = Field(default=0, ge=0, le=10)
    source_id: str = Field(default="")
    type: str = Field(default="movie")
