from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.review import (
    AddReviewRequest,
    AddReviewResponse,
#     GetReviewsForPlaceRequest,
#     GetReviewsForPlaceResponse,
#     ModerateReviewsRequest,
#     ModerateReviewsResponse,
#     GetReviewsForModerateRequest,
#     GetReviewsForModerateResponse,
#     GetReviewsRequest,
#     GetReviewsResponse,
#     GetCountOfReviewsRequest,
#     GetCountOfReviewsResponse,
)
from app.service.use_cases.reviews.reviews import ReviewService
from app.db.repositories.reviews import ReviewRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.place import PlaceRepository
from app.db.repositories.plase_stats import PlaceStatsRepository

router = APIRouter(prefix="/review", tags=["review"])

def get_review_repository(
    session: Session = Depends(get_db),
) -> ReviewRepository:
    return ReviewRepository(session)

def get_user_repository(
    session: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)

def get_place_repository(
    session: Session = Depends(get_db),
) -> PlaceRepository:
    return PlaceRepository(session)

def get_place_stats_repository(
    session: Session = Depends(get_db),
) -> PlaceStatsRepository:
    return PlaceStatsRepository(session)

def get_review_service(
    review_repo: ReviewRepository = Depends(get_review_repository),
    place_repo: PlaceRepository = Depends(get_place_repository),
    place_stats_repo: PlaceStatsRepository = Depends(get_place_stats_repository),
) -> ReviewService:
    return ReviewService(review_repo=review_repo, place_repo=place_repo, place_stats_repo=place_stats_repo)

@router.post("/add", response_model=AddReviewResponse)
def add_review(
    data: AddReviewRequest,
    service: ReviewService = Depends(get_review_service)
):
    return service.add_review(data.dto, data.user)