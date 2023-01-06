from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

router = APIRouter()


class Event(BaseModel):
    """Валидатор данных о просмотре фильма."""

    event_name: str = Field(default="Название события")
    event_value: str = Field(default="Значение события")


async def get_id(user_id, film_id):
    return user_id + "-" + film_id


@router.post(
    "/{film_id}/events",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def film_events(film_id: str, event: Event, request: Request) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
    Returns:
        Статус выполнения.
    """
    if not hasattr(request.state, "id_user"):
        return "User not found"
    id = await get_id(request.state.id_user, film_id)

    return "status"
