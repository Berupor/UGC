from http import HTTPStatus
from typing import Dict, List

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from fastapi import APIRouter, Depends, HTTPException
from models.rating import Rating
from models.user import User
from services.base_service import EventService, get_event_service
from services.rating_service import RatingService, get_rating_service

router = APIRouter()


@router.post(
    "/{source_id}",
    summary="Создание оценки фильма или рецензии",
    description="Пользователь передаёт оценку на фильм или рецензию. Выбор объекта оценки определяется параметрами body. ",
    response_description="Статус обработки данных",
)
@exception_handler
async def add_rating(
    event: Rating,
    source_id: str,
    event_service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
):
    """Processing getting event data.
    Args:
        source_id: Id current film.
        event: event data.
        request: request value.
        event_service: login execution by endpoint.
        user_id: Id user
    Returns:
        Execution status.
    """
    event.user_id = str(user_id)
    event.source_id = source_id

    await event_service.produce(key=source_id, topic_name="rating", data=event)
    return HTTPStatus.CREATED


@router.get(
    "/{source_id}",
    summary="Получение оценки фильма или рецензии",
    description="Пользователь получает все оценки на фильм или рецензию. Выбор объекта оценки определяется параметрами body. ",
    response_description="Статус обработки данных",
)
@exception_handler
async def get_ratings(
    source_id: str, rating_service: RatingService = Depends(get_rating_service)
) -> List[Dict]:
    ratings = rating_service.find({"source_id": source_id})
    return [review async for review in ratings]


@router.delete(
    "/{source_id}",
    summary="Удаление оценки фильма или рецензии",
    description="Удаление оценки на фильм или рецензию. Выбор объекта оценки определяется параметрами body. ",
    response_description="Статус обработки данных",
)
@exception_handler
async def delete_review_rating(
    source_id: str,
    rating_service: RatingService = Depends(get_rating_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await rating_service.delete_one(
        {"source_id": source_id, "user_id": str(user_id)}
    )
    if result:
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=404, detail="Rating not found")
