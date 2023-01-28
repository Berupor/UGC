from pydantic import Field

from models.base import BaseOrjson


class RatingFilm(BaseOrjson):
    rating: float = Field(default=0, ge=0, le=10)
