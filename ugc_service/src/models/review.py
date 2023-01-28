from uuid import UUID

from bson import ObjectId
from pydantic import Field as PydanticField

from models.base import BaseEventModel
from models.object_id import PyObjectId


class ShortReview(BaseEventModel):
    text: str
    movie_id: UUID
    author_id: UUID
    id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}


class FullReview(ShortReview):
    ...
