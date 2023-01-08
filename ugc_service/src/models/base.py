from fastapi import Request
from pydantic import BaseModel, Field
import orjson
from uuid import UUID


#
def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseEventModel(BaseModel):
    """Base class"""
    timestamp_ms: int = Field(default=0, ge=-2177452799, le=4102444801)

    async def get_key(self, request: Request, film_id: UUID) -> str:
        return request.state.id_user + "-" + film_id

    class Config:
        # We replace the standard work with json with a faster one
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseEventValue(BaseModel):
    """Base value class"""

    class Config:
        # We replace the standard work with json with a faster one
        json_loads = orjson.loads
        json_dumps = orjson_dumps



