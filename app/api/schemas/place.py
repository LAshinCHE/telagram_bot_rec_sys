from pydantic import BaseModel
from app.domain.enum import PlaceStatus


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
