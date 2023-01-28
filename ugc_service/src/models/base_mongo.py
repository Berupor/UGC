from bson import ObjectId
from pydantic import Extra, Field as PydanticField
from uuid import UUID
from models.base import BaseEventModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseMongoModel(BaseEventModel):
    id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")
    author_id: str = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
