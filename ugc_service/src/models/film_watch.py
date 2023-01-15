from pydantic import Field

from models.base import BaseEventModel


class FilmWatchEvent(BaseEventModel):
    viewpoint: int = Field(default=0, ge=-2177452799, le=4102444801)
