from fastapi import APIRouter, Depends, Request
from services.review_service import get_review_service, ReviewService
from pydantic import BaseModel

review = APIRouter()


class Review(BaseModel):
    text: str
    author: str
    publication_date: str
    rating: float
    likes_or_dislikes: str


@review.post("/movies/{movie_id}/reviews")
async def add_review(movie_id: str, review: Review,
                     service: ReviewService = Depends(get_review_service("movies", "reviews")),

                     ):
    review_document = review.dict()
    review_document["movie_id"] = movie_id
    service.create(review_document)
    return {"message": "Review added successfully."}
