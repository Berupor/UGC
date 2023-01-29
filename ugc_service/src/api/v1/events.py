from http import HTTPStatus
from typing import Tuple

from fastapi import APIRouter, Depends, Request

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from models.film_watch import FilmWatchEvent
from models.user import User
from services.base_service import EventService, get_event_service

router = APIRouter()


@router.post(
    "/{movie_id}/viewpoint",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
@exception_handler
async def viewpoint_film(
    event: FilmWatchEvent,
    movie_id,
    request: Request,
    service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
):
    """Обработка полученных данных о событии.
    Args:
        movie_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
        service: Сервис для работы с Кафка.
    Returns:
        Execution status.
        user_id: Id пользователя
    """
    await service.produce(key=f"{user_id}&{movie_id}", topic_name="views", data=event)
    return HTTPStatus.CREATED
