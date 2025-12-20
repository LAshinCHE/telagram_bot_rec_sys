from pydantic import BaseModel, Field

class AddReviewDTO(BaseModel):
    place_id: int
    rating: int = Field(ge=1, le=5)
    text: str