from pydantic import Field

from models.base import BaseOrjson


class Bookmarks(BaseOrjson):
    status: bool = Field(default=True)
