from fastapi import APIRouter, Depends, HTTPException
from services.review_service import get_review_service, ReviewService
from services.base_service import EventService, get_event_service
from pydantic import BaseModel
from bson.objectid import ObjectId

router = APIRouter()


class ShortReview(BaseModel):
    text: str
    author: str
    publication_date: str


class FullReview(BaseModel):
    text: str
    author: str
    publication_date: str
    movie_id: str


@router.post("/{movie_id}")
async def add_review(
    movie_id: str,
    review: ShortReview,
    review_service: ReviewService = Depends(get_review_service),
    event_service: EventService = Depends(get_event_service),
):
    review_document = review.dict()
    review_document["movie_id"] = movie_id

    await review_service.insert_one(review_document)

    # await event_service.produce(key=movie_id, topic_name="reviews", model=review_document)

    return {"message": "Review added successfully."}


@router.get("/{movie_id}")
async def get_all_reviews(
    movie_id: str, review_service: ReviewService = Depends(get_review_service)
):
    reviews = review_service.find({"movie_id": movie_id})

    return [FullReview(**review) async for review in reviews]


@router.put("/{review_id}")
async def update_review(
    review_id: str,
    review: ShortReview,
    review_service: ReviewService = Depends(get_review_service),
):
    review_id = ObjectId(review_id)

    result = await review_service.update_one(
        {"_id": review_id}, {"$set": review.dict()}
    )
    if result:
        return {"message": "Review updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Review not found")


@router.delete("/{review_id}")
async def delete_review(
    review_id: str, review_service: ReviewService = Depends(get_review_service)
):
    review_id = ObjectId(review_id)

    result = await review_service.delete_one({"_id": review_id})
    if result:
        return {"message": "Review deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Review not found")
