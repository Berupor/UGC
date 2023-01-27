from http import HTTPStatus

from api.v1.auth_bearer import JWTBearer
from api.v1.decorators import exception_handler
from fastapi import APIRouter, Depends, Request
from models.rating import RatingFilm
from models.user import User
from services.base_service import EventService, get_event_service
from typing import Tuple

router = APIRouter()


@router.post(
    "/{film_id}",
    summary="Получение оценки фильма",
    description="Получение оценки фильма от пользователя.",
    response_description="Статус обработки данных",
)
@exception_handler
async def rating_film(
    event: RatingFilm,
    film_id,
    request: Request,
    service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
) -> Tuple[str, int]:
    """Processing received event data.
    Args:
        film_id: Id current film.
        event: event data.
        request: request value.
        service: login execution by endpoint.
        user_id: Id user
    Returns:
        Execution status.
    """
    key = await event.get_key(user_id, film_id)
    await service.produce(key=key, topic_name="rating", model=event)
    return HTTPStatus.OK.phrase, 200