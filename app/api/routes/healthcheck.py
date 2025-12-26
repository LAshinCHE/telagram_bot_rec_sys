from fastapi import APIRouter
from app.service.use_cases.healthcheck import healthcheck_service

router = APIRouter()

@router.get("/health", tags=["Healthcheck"])
def healthcheck():
    return healthcheck_service()
