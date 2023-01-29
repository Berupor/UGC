from pydantic import Field

from models.base_mongo import BaseMongoModel


class Bookmark(BaseMongoModel):
    movie_id: str
    status: bool = Field(default=True)
