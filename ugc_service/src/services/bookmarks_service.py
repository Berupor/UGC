from .base_mongo_service import BaseMongoService


class BookmarksService(BaseMongoService):
    pass


def get_bookmarks_service() -> BookmarksService:
    return BookmarksService("movies", "bookmarks")
