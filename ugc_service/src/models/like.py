from pydantic import Field

from models.base import BaseEventModel, BaseEventValue


class LikeValue(BaseEventValue):
    like: bool = Field(default=False)


class LikeEvent(BaseEventModel):
    value: LikeValue
