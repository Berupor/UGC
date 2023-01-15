from models.base import BaseEventModel, BaseEventValue
from pydantic import Field


class LikeValue(BaseEventValue):
    like: bool = Field(default=False)


class LikeEvent(BaseEventModel):
    value: LikeValue
