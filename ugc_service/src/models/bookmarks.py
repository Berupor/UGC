from models.base_mongo import BaseMongoModel
from pydantic import Field


class Bookmark(BaseMongoModel):
    movie_id: str = ""
    status: bool = Field(default=True)
