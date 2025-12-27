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
    place_id = service.create_place(place=place)
    responce = CreatePlaceResponce(id=place_id)
    return responce

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/{place_id}", response_model=GetPlaceResponce)
def get_place_by_id(
    place_id: int,
    user_id: int,
    service: PlaceService = Depends(get_place_service),
):
    place = service.get_place(place_id)

    responce = GetPlaceResponce(
            id=place.id,
            name=place.name,
            city=place.city,
            address_text=place.address_text,
            price_level=place.price_level,
            created_by=place.created_by
    )

    return responce