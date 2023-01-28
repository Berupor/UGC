from pydantic import Field

from models.base import BaseEventModel


class Bookmarks(BaseEventModel):
    status: bool = Field(default=True)
