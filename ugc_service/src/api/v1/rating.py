from http import HTTPStatus
from typing import Dict, List, Type

from fastapi import APIRouter, Depends, HTTPException, Path

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from models.base_mongo import PyObjectId
from models.rating import MovieRating, Rating, ReviewRating
from models.user import User
from services.base_service import EventService, get_event_service
from services.rating_service import RatingService, get_rating_service

router = APIRouter()


async def get_ratings(
    filter: Dict,
    rating_class: Type[Rating],
    rating_service: RatingService = get_rating_service(),
) -> List[Rating]:
    ratings = rating_service.find(filter)
    return [rating_class(**review) async for review in ratings]


@router.post(
    "/movie/{movie_id}",
    summary="Создание оценки фильма",
    description="Создание оценки фильма от пользователя.",
    response_description="Статус обработки данных",
)
@exception_handler
async def add_movie_rating(
    event: MovieRating,
    movie_id: str,
    event_service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
):
    """Processing getting event data.
    Args:
        movie_id: Id current film.
        event: event data.
        request: request value.
        event_service: login execution by endpoint.
        user_id: Id user
    Returns:
        Execution status.
    """
    event.user_id = str(user_id)
    event.movie_id = movie_id

    await event_service.produce(key=movie_id, topic_name="rating", data=event)
    return HTTPStatus.CREATED


@router.get("/movie/{movie_id}")
@exception_handler
async def get_all_movie_ratings(movie_id: str) -> List[Rating]:
    return await get_ratings({"movie_id": movie_id}, MovieRating)


@router.delete("/movie/{rating_id}")
@exception_handler
async def delete_movie_rating(
    rating_id: PyObjectId = Path(..., alias="rating_id"),
    rating_service: RatingService = Depends(get_rating_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await rating_service.delete_one(
        {"_id": rating_id, "user_id": str(user_id)}
    )
    if result:
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=404, detail="Rating not found")


@router.post(
    "/review/{review_id}",
)
@exception_handler
async def add_review_rating(
    event: ReviewRating,
    review_id: PyObjectId = Path(..., alias="review_id"),
    event_service: EventService = Depends(get_event_service),
    rating_service: RatingService = Depends(get_rating_service),
    user_id: User = Depends(JWTBearer()),
):
    event.user_id = str(user_id)
    event.review_id = review_id

    await rating_service.insert_one(event.dict())
    await event_service.produce(key=str(review_id), topic_name="rating", data=event)
    return HTTPStatus.CREATED


@router.get("/review/{review_id}")
@exception_handler
async def get_all_review_ratings(
    review_id: PyObjectId = Path(..., alias="review_id")
) -> List[Rating]:
    return await get_ratings({"review_id": review_id}, ReviewRating)


@router.delete("/review/{rating_id}")
@exception_handler
async def delete_review_rating(
    rating_id: PyObjectId = Path(..., alias="rating_id"),
    rating_service: RatingService = Depends(get_rating_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await rating_service.delete_one(
        {"_id": rating_id, "user_id": str(user_id)}
    )
    if result:
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=404, detail="Rating not found")
