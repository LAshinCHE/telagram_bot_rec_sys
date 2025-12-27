# app/api/routes/recommendations.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.recommendations import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.db.repositories.reviews import ReviewRepository
from app.recommendation.recommendation_service import Recommendation
from app.service.use_cases.llm.recommendation import RecommendationService
from app.db.session import get_db
from app.db.repositories.place import PlaceRepository
from app.db.repositories.tag import TagRepository
from app.llm.llm_entities import LLM_Entities
from app.llm.llm_generation_answer import LLM_Generation
from app.settings import settings

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecommendationService:
    place_repo = PlaceRepository(db)

    # 1. Инициализируем репозиторий тегов и получаем список имен
    tag_repo = TagRepository(db)
    all_tags_entities = tag_repo.get_all()

    allowed_tags = [tag.name for tag in all_tags_entities] if all_tags_entities else []

    print(allowed_tags)

    llm = LLM_Entities(
        LM_STUDIO_URL=settings.LM_STUDIO_URL,
        API_KEY=settings.API_KEY,
        ALLOWED_TAGS=allowed_tags,
        DEFAULT_MODEL=settings.DEFAULT_MODEL,
    )

    recommendation_repo = ReviewRepository(db)

    recommendation = Recommendation("svd_model.pkl")

    generation_llm = LLM_Generation(LM_STUDIO_URL=settings.LM_STUDIO_URL,
                                    API_KEY=settings.API_KEY,
                                    MODEL_NAME=settings.DEFAULT_MODEL)


    return RecommendationService(
        place_repo=place_repo,
        llm_entities=llm,
        recommendation_repo=recommendation_repo,
        recommendation=recommendation,
        generation_llm=generation_llm,
    )


@router.post("/", response_model=RecommendationResponse)
def recommend_places(
    data: RecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service),
):
    return service.recommend(data.query, data.user_id)
