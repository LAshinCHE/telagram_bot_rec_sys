# app/api/schemas/recommendation.py
from pydantic import BaseModel
from typing import List, Optional


class RecommendationRequest(BaseModel):
    user_id: str
    query: str


class PlaceResponse(BaseModel):
    id: int
    name: str
    city: str
    price_level: Optional[int]
    rating_avg: Optional[float]
    rating_cnt: int
    tags: List[str]


class RecommendationResponse(BaseModel):
    # filters: dict
    places: List[PlaceResponse]
    answer: str
