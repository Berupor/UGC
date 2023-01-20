from datetime import datetime
from uuid import UUID
from models.user import User

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes and pydantic requires unicode so decode
    return orjson.dumps(v, default=default).decode()


class BaseEventModel(BaseModel):
    datetime_event: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    async def get_key(self, user_id: User, film_id: UUID) -> str:
        return f"{user_id}&{film_id}"

    class Config:
        # We replace the standard work with json with a faster one
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseEventValue(BaseModel):
    """Base value class"""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
