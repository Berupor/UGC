from fastapi import Request
from pydantic import BaseModel, Field


class Events(BaseModel):
    """Base class for events."""

    async def get_user_id(self, request: Request):
        if not hasattr(request.state, "id_user"):
            return None
        return request.state.id_user

    async def get_id(self, user_id: str, film_id: str) -> str:
        return user_id + "-" + film_id


class ViewPointFilm(Events):
    viewpoint: int = Field(default=0, ge=-2177452799, le=4102444801)


class LikeFilm(Events):
    like: bool = Field(default=False)


class CommentFilm(Events):
    comment: str = Field(default="comment", max_length=8000)


class RatingFilm(Events):
    like: float = Field(default=10, ge=0, lt=10)
