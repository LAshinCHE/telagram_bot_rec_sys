from fastapi import APIRouter
from app.service.healthcheck import healthcheck_service

router = APIRouter()

@router.get("/health", tags=["Healthcheck"])
def healthcheck():
    return healthcheck_service()
