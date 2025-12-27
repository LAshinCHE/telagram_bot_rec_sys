from pydantic import BaseModel
from app.domain.enum import ReviewStatus, UserRole
from datetime import datetime
from typing import List, Optional

class dto(BaseModel):
    place_id: int
    rating: int
    text: str

class user(BaseModel):
    id: int
    role: UserRole

class AddReviewRequest(BaseModel):
    dto: dto
    user: user

class Review(BaseModel):
    place_id: int
    author_id: int
    author_id: int
    rating: int
    text: str
    status: ReviewStatus
    moderated_by: int
    moderated_at: datetime
    created_at: datetime

class AddReviewResponse(BaseModel):
    review: Review

# class GetReviewsForPlaceRequest(BaseModel):
#     place_id: int

# class GetReviewsForPlaceResponse(BaseModel):
#     reviews: List[Review]

# class ModerateReviewsRequest(BaseModel):
#     review_id: int
#     moderator_id: int
#     status: ReviewStatus

# class ModerateReviewsResponse(BaseModel):
#     review: Review

# class GetReviewsForModerateRequest(BaseModel):
#     pass

# class GetReviewsForModerateResponse(BaseModel):
#     reviews: List[Review]

# class GetReviewsRequest(BaseModel):
#     x: 4

# class GetReviewsResponse(BaseModel):
#     reviews: List[Review]

# class GetCountOfReviewsRequest(BaseModel):
#     place_id: int

# class GetCountOfReviewsResponse(BaseModel):
#     count: int

