from fastapi import Request
from pydantic import BaseModel, Field
import orjson


# class Events(BaseModel):
#     """Base class for events."""
#
#     async def get_user_id(self, request: Request):
#         if not hasattr(request.state, "id_user"):
#             return None
#         return request.state.id_user
#
#     async def get_id(self, user_id: str, film_id: str) -> str:
#         return user_id + "-" + film_id
#
def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseEventModel(BaseModel):
    """Base class"""

    class Config:
        # We replace the standard work with json with a faster one
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmWatchValue(BaseEventModel):
    # viewpoint: int = Field(default=0, ge=-2177452799, le=4102444801)
    watched_seconds: str


class FilmWatch(BaseEventModel):
    value: FilmWatchValue
    timestamp_ms: str
    # timestamp_ms: int = Field(default=0, ge=-2177452799, le=4102444801)

# class LikeFilm(BaseEventModel):
#     like: bool = Field(default=False)
#
#
# class CommentFilm(BaseEventModel):
#     comment: str = Field(default="comment", max_length=8000)
#
#
# class RatingFilm(BaseEventModel):
#     like: float = Field(default=10, ge=0, lt=10)
