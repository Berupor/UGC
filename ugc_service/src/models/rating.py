from pydantic import Field

from models.base import BaseEventModel


class RatingFilm(BaseEventModel):
    rating: float = Field(default=0, ge=0, le=10)