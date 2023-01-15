from pydantic import Field

from models.base import BaseEventModel, BaseEventValue


class RatingValue(BaseEventValue):
    like: float = Field(default=10, ge=0, lt=10)


class RatingEvent(BaseEventModel):
    value: RatingValue
