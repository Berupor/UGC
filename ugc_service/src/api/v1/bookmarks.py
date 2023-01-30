from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from models.base_mongo import PyObjectId
from models.bookmarks import Bookmark
from models.user import User
from typing import List
from services.base_service import EventService, get_event_service
from services.bookmarks_service import BookmarksService, get_bookmarks_service

router = APIRouter()


@router.post(
    "/{movie_id}",
)
@exception_handler
async def add_bookmark(
        event: Bookmark,
        movie_id: str,
        service: EventService = Depends(get_event_service),
        user_id: User = Depends(JWTBearer()),
        bookmark_service: BookmarksService = Depends(get_bookmarks_service)
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

    # await bookmark_service.insert_one(event.dict())
    await service.produce(key=movie_id, topic_name="bookmarks", data=event)
    return HTTPStatus.CREATED


@router.get("/")
@exception_handler
async def get_all_bookmarks(
        bookmark_service: BookmarksService = Depends(get_bookmarks_service),
        user_id: User = Depends(JWTBearer()),
) -> List[dict]:
    bookmarks = bookmark_service.find({"user_id": user_id})

    return [bookmark async for bookmark in bookmarks]


@router.delete("/{bookmark_id}")
@exception_handler
async def delete_bookmark(
        bookmark_id: PyObjectId = Path(..., alias="bookmark_id"),
        bookmark_service: BookmarksService = Depends(get_bookmarks_service),
        user_id: User = Depends(JWTBearer()),
):
    result = await bookmark_service.delete_one({"id": bookmark_id, "user_id": user_id})
    if result:
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=404, detail="Review not found")
