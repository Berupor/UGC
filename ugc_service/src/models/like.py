from models.base import BaseEventModel, BaseEventValue
from pydantic import Field


class LikeFilmValue(BaseEventValue):
    like: bool = Field(default=False)


class LikeFilmEvent(BaseEventModel):
    value: LikeFilmValue
