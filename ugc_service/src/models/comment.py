from pydantic import Field

from models.base import BaseEventModel, BaseEventValue


class CommentValue(BaseEventValue):
    comment: str = Field(default="comment", max_length=8000)


class CommentEvent(BaseEventModel):
    value: CommentValue
