from datetime import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel, Field

from models.user import User


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseEventModel(BaseModel):
    datetime_event: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
