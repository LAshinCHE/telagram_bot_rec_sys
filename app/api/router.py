from fastapi import APIRouter
from app.api.routes import healthcheck, place, recommendation, user, review, tag

api_router = APIRouter()
api_router.include_router(healthcheck.router)
api_router.include_router(place.router)
api_router.include_router(user.router)
api_router.include_router(recommendation.router)
api_router.include_router(review.router)
api_router.include_router(tag.router)