from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from models.events import CommentFilm, LikeFilm, RatingFilm, ViewPointFilm

router = APIRouter()


@router.post(
    "/{film_id}/viewpoint",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def viewpoint_film(film_id: str, event: ViewPointFilm, request: Request) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
    Returns:
        Статус выполнения.
    """
    id_user = await event.get_user_id(request)
    if not id_user:
        return "User not found"
    id = await event.get_id(id_user, film_id)
    print('\n\n\n', id)

    return "status"


@router.post(
    "/{film_id}/like",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def like_film(film_id: str, event: LikeFilm, request: Request) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
    Returns:
        Статус выполнения.
    """
    id_user = await event.get_user_id(request)
    if not id_user:
        return "User not found"
    id = await event.get_id(id_user, film_id)

    return "status"


@router.post(
    "/{film_id}/comment",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def comment_film(film_id: str, event: CommentFilm, request: Request) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
    Returns:
        Статус выполнения.
    """
    id_user = await event.get_user_id(request)
    if not id_user:
        return "User not found"
    id = await event.get_id(id_user, film_id)

    return "status"


@router.post(
    "/{film_id}/rating",
    summary="Получение отметки о просмотре фильма",
    description="Получение данных о том, сколько времени пользователь посмотрел фильм.",
    response_description="Статус обработки данных",
)
async def rating_film(film_id: str, event: RatingFilm, request: Request) -> str:
    """Обработка полученных данных о событии.
    Args:
        film_id: Id текущего фильма.
        event: Данные о событии.
        request: Значения запроса.
    Returns:
        Статус выполнения.
    """
    id_user = await event.get_user_id(request)
    if not id_user:
        return "User not found"
    id = await event.get_id(id_user, film_id)

    return "status"
