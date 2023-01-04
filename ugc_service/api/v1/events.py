from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


class EventTimestamp(BaseModel):
    """Валидатор данных о просмотре фильма."""

    id_user: str
    timestamp: int
    film_duration: int


@router.post(
    "/{film_id}/episodes",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def film_episodes(
    film_id: str,
    event_timestamp: EventTimestamp
) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
    Returns:
        Объект фильма.
    """

    return "status"
