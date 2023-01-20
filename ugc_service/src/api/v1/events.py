from http import HTTPStatus

from api.v1.auth_bearer import JWTBearer
from api.v1.decorators import exception_handler
from fastapi import APIRouter, Depends, Request
from models.film_watch import FilmWatchEvent
from models.user import User
from services.base_service import EventService, get_event_service

router = APIRouter()


@router.post(
    "/{film_id}/viewpoint",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
@exception_handler
async def viewpoint_film(
    event: FilmWatchEvent,
    film_id,
    request: Request,
    service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
) -> tuple[str, int]:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
        service: Сервис для работы с Кафка.
    Returns:
        Execution status.
        user_id: Id пользователя
    """
    key = await event.get_key(user_id, film_id)
    await service.produce(key=key, topic_name="views", model=event)
    return HTTPStatus.OK.phrase, 200
