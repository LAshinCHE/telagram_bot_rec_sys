from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.schemas.place import (
    CreatePlaceRequest,
    CreatePlaceResponce,
    GetPlaceRequest,
    GetPlaceResponce,
)

from app.service.use_cases.place.place import PlaceService
from app.db.session import get_db
from app.db.repositories.place import PlaceRepository
from app.domain.enum import PlaceStatus
from app.domain.entities.place import Place

router = APIRouter()


router = APIRouter(prefix="/places", tags=["places"])
def get_place_service(
    db: Session = Depends(get_db),
) -> PlaceService:
    place_repo = PlaceRepository(db)


    return PlaceService(
        place_repo=place_repo,
    )


@router.post("/", response_model=CreatePlaceResponce)
def recommend_places(
    data: CreatePlaceRequest,
    user_id: int,
    service: PlaceService = Depends(get_place_service),
):
    place = Place(
            id=None, 
            name=data.name,
            description=data.description, 
            city=data.city,
            address_text=data.address_text,
            price_level=data.price_level,
            status=PlaceStatus.ACTIVE,
            created_by=user_id,
            created_at=datetime.now()
        )
    return service.create_place(place=place)

@router.get("/", response_model=GetPlaceResponce)
def recommend_places(
    data: GetPlaceRequest,
    user_id: int,
    service: PlaceService = Depends(get_place_service),
):
    return service.get_place(data.id)
 
 