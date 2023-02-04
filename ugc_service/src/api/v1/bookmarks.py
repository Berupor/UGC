from http import HTTPStatus
from typing import List, Dict

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from fastapi import APIRouter, Depends, HTTPException, Request
from models.bookmarks import Bookmark
from models.user import User
from services.base_service import EventService, get_event_service
from services.bookmarks_service import BookmarksService, get_bookmarks_service

router = APIRouter()


@router.post(
    "/{movie_id}",
    summary="Добавление фильма в закладки.",
    description="Добавление текущего фильма в закладки пользователя.",
    response_description="Статус обработки данных",
)
@exception_handler
async def add_bookmark(
    event: Bookmark,
    movie_id,
    request: Request,
    service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
):
    """Processing received event data.
    Args:
        movie_id: Id current film.
        event: event data.
        request: request value.
        service: login execution by endpoint.
        user_id: Id user
    Returns:
        Execution status.
    """
    event.user_id = str(user_id)
    event.movie_id = movie_id

    await service.produce(key=movie_id, topic_name="bookmarks", data=event)

    return HTTPStatus.CREATED


@router.get(
    "/",
    summary="Получение фильмов, добавленных в закладки.",
    description="Получение всех фильмов, которые пользователь ранее добавил в закладки.",
    response_description="Статус обработки данных",
)
async def get_all_bookmarks(
    user_id: User = Depends(JWTBearer()),
    bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
) -> List[Dict]:
    bookmarks = bookmarks_service.find({"user_id": user_id})
    return [bookmark async for bookmark in bookmarks]


@router.delete(
    "/{movie_id}",
    summary="Удаление фильма из закладок.",
    description="Убрать текущей фильм из списка 'закладки'.",
    response_description="Статус обработки данных",
)
async def delete_movie_bookmark(
    movie_id: str,
    bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await bookmarks_service.delete_one(
        {"movie_id": movie_id, "user_id": user_id}
    )
    if result:
        return HTTPStatus.NO_CONTENT
    else:
        raise HTTPException(status_code=404, detail="Rating not found")

