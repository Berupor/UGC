from http import HTTPStatus
from typing import Dict, List

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from fastapi import APIRouter, Depends, HTTPException, Query
from models.review import ShortReview
from models.user import User
from services.base_service import EventService, get_event_service
from services.review_service import ReviewService, get_review_service

router = APIRouter()


@router.post("/{movie_id}")
@exception_handler
async def add_review(
    movie_id: str,
    event: ShortReview,
    event_service: EventService = Depends(get_event_service),
    user_id: User = Depends(JWTBearer()),
):
    event.user_id = str(user_id)
    event.movie_id = movie_id

    await event_service.produce(key=movie_id, topic_name="reviews", data=event)

    return HTTPStatus.CREATED


@router.get("/{movie_id}")
@exception_handler
async def get_all_reviews(
    movie_id: str,
    sort: str = Query(default="likes", alias="sort"),
    review_service: ReviewService = Depends(get_review_service),
) -> List[Dict]:
    reviews = review_service.find(
        {"movie_id": movie_id},
        sort_field=sort[1:],
        order=-1 if sort.startswith("-") else 1,
    )
    return [review async for review in reviews]


@router.delete("/{review_id}")
@exception_handler
async def delete_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await review_service.delete_one({"id": review_id, "user_id": user_id})
    if result:
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=404, detail="Review not found")
