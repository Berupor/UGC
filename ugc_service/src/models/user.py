from uuid import UUID

from models.base import BaseOrjson


class User(BaseOrjson):
    user_id: UUID
