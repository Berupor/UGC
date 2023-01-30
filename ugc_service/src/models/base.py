from datetime import datetime

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class BaseEventModel(BaseModel):
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
