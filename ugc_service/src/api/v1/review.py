from http import HTTPStatus

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from api.v1.auth_bearer import JWTBearer
from models.review import ShortReview, FullReview
from models.user import User
from services.base_service import EventService, get_event_service
from services.review_service import get_review_service, ReviewService

router = APIRouter()


@router.post("/{movie_id}")
async def add_review(
        movie_id: str,
        event: ShortReview,
        event_service: EventService = Depends(get_event_service),
        review_service: ReviewService = Depends(get_review_service),
        user_id: User = Depends(JWTBearer())
):
    event.author_id = user_id
    event.movie_id = movie_id

    await review_service.insert_one(event.dict())
    await event_service.produce(key=movie_id, topic_name="reviews", data=event)

    return HTTPStatus.CREATED


@router.get("/{movie_id}")
async def get_all_reviews(
        movie_id: str, review_service: ReviewService = Depends(get_review_service)
) -> list[FullReview]:
    reviews = review_service.find({"movie_id": movie_id})

    return [FullReview(**review) async for review in reviews]


# @router.put("/{review_id}")
# async def update_review(
#         review_id: str,
#         review: ShortReview,
#         review_service: ReviewService = Depends(get_review_service),
# ):
#     review_id = ObjectId(review_id)
#
#     result = await review_service.update_one(
#         {"_id": review_id}, {"$set": review.dict()}
#     )
#     if result:
#         return {"message": "Review updated successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Review not found")


@router.delete("/{review_id}")
async def delete_review(
        review_id: str, review_service: ReviewService = Depends(get_review_service),
        user_id: User = Depends(JWTBearer())
):
    result = await review_service.delete_one({"_id": ObjectId(review_id), "author_id": user_id})
    if result:
        return HTTPStatus.NO_CONTENT
    else:
        raise HTTPException(status_code=404, detail="Review not found")


