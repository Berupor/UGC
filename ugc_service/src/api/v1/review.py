from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from api.v1.utils.auth_bearer import JWTBearer
from api.v1.utils.decorators import exception_handler
from models.review import FullReview, ShortReview
from models.user import User
from services.base_service import EventService, get_event_service
from services.review_service import ReviewService, get_review_service

router = APIRouter()


@exception_handler
@router.post("/{movie_id}")
async def add_review(
    movie_id: str,
    event: ShortReview,
    event_service: EventService = Depends(get_event_service),
    review_service: ReviewService = Depends(get_review_service),
    user_id: User = Depends(JWTBearer()),
):
    event.user_id = str(user_id)
    event.movie_id = movie_id

    await review_service.insert_one(event.dict())
    await event_service.produce(key=movie_id, topic_name="reviews", data=event)

    return HTTPStatus.CREATED


@exception_handler
@router.get("/{movie_id}")
async def get_all_reviews(
    movie_id: str,
    review_service: ReviewService = Depends(get_review_service),
) -> List[FullReview]:

    reviews = review_service.find({"movie_id": movie_id})
    # return {'sussecc'}
    return [FullReview(**review) async for review in reviews]


@exception_handler
@router.delete("/{review_id}")
async def delete_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service),
    user_id: User = Depends(JWTBearer()),
):
    result = await review_service.delete_one(
        {"_id": ObjectId(review_id), "user_id": user_id}
    )
    if result:
        return HTTPStatus.NO_CONTENT
    else:
        raise HTTPException(status_code=404, detail="Review not found")
