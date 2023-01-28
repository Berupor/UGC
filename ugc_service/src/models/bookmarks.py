from pydantic import Field

from models.base_mongo import BaseMongoModel


class Bookmarks(BaseMongoModel):
    status: bool = Field(default=True)
