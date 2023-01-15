from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from api.v1.decorators import exception_handler
from models.film_watch import FilmWatchEvent
from services.base import EventService, get_event_service

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
) -> tuple[str, int]:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
        service: Сервис для работы с Кафка.
    Returns:
        Статус выполнения.
    """
    key = await event.get_key(request, film_id)
    await service.produce(key=key, topic_name="views", model=event)
    return HTTPStatus.OK.phrase, 200
