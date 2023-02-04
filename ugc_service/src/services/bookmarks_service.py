from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .base_mongo_service import BaseMongoService, get_database_conn


class BookmarksService(BaseMongoService):
    pass


def get_bookmarks_service(
    database_conn: AsyncIOMotorClient = Depends(get_database_conn),
) -> BookmarksService:
    return BookmarksService("movies", "bookmarks", database_conn)
