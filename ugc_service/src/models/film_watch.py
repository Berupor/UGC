from models.base import BaseEventModel, BaseEventValue
from pydantic import Field


class FilmWatchValue(BaseEventValue):
    watched_seconds: int = Field(default=0, ge=-2177452799, le=4102444801)


class FilmWatchEvent(BaseEventModel):
    value: FilmWatchValue
