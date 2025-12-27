from pydantic import BaseModel
from app.domain.enum import PlaceStatus
from typing import Optional, List
from datetime import datetime



class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CreatePlaceRequest(BaseModel):
    id: int
    name: str
    description: str
    city: str
    address_text: str
    price_level: int

class CreatePlaceResponce(BaseModel):
    id: int

class GetPlaceRequest(BaseModel):
    id: int

class GetPlaceResponce(BaseModel):
    id: int
    name: str
    city: str
    address_text: str
    price_level: int
    created_by: int

class AddPlaceTagRequest(BaseModel):
    place_id: int
    list_tags_id: list[int]

class AddPlaceTagResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    city: str
    address_text: Optional[str]
    price_level: Optional[int]
    status: str
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]

    tags: List[TagOut]

    class Config:
        from_attributes = True