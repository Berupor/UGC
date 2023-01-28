from http import HTTPStatus

from api.v1.auth_bearer import JWTBearer
from api.v1.decorators import exception_handler
from fastapi import APIRouter, Depends, Request
from models.bookmarks import Bookmarks
from models.user import User
from services.base_service import EventService, get_event_service
from typing import Tuple

router = APIRouter()


@router.post(
    "/{movie_id}",
    summary="Закладки пользователя",
    description="",
    response_description="",
)
@exception_handler
async def bookmarks(
    event: Bookmarks,
    movie_id,
    request: Request,
    service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
) -> Tuple[str, int]:
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
    key = await event.get_key(user_id, movie_id)
    await service.produce(key=key, topic_name="bookmarks", model=event)
    return HTTPStatus.OK.phrase, 200