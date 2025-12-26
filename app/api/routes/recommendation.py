# app/api/routes/recommendations.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.recommendations import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.service.use_cases.llm.recommendation import RecommendationService
from db.session import get_db
from db.repositories.place import PlaceRepository
from app.llm.llm_entities import LLM_Entities
from app.setings import settings

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecommendationService:
    place_repo = PlaceRepository(db)

    llm = LLM_Entities(
        LM_STUDIO_URL=settings.LM_STUDIO_URL,
        API_KEY=settings.LM_API_KEY,
        ALLOWED_TAGS=settings.ALLOWED_TAGS,
        DEFAULT_MODEL=settings.LLM_MODEL,
    )

    return RecommendationService(
        place_repo=place_repo,
        llm_entities=llm,
    )


@router.post("/", response_model=RecommendationResponse)
def recommend_places(
    data: RecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service),
):
    return service.recommend(data.query, data.user_id)
