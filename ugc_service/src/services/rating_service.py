from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .base_mongo_service import BaseMongoService, get_database_conn


class RatingService(BaseMongoService):
    pass


def get_rating_service(
    database_conn: AsyncIOMotorClient = Depends(get_database_conn),
) -> RatingService:
    return RatingService("movies", "rating", database_conn)
