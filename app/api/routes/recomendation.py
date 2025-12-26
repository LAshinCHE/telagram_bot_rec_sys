from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.service.use_cases.llm.recommendation import RecomendationService
from db.session import get_db
from db.repositories.reviews import ReviewRepository
from app.recommendation.recommendation_service import Recomendation

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecomendationService:
    repo = ReviewRepository(db)
    model = Recomendation()
    return RecomendationService(
        recomendation_repo=repo,
        recomendation=model,
    )


@router.post("/")
def get_recommendations(
    user_id: int,
    place_ids: list[int],
    service: RecomendationService = Depends(get_recommendation_service),
):
    return service.get_rank_place(
        user_id=user_id,
        place_ids=place_ids,
    )
