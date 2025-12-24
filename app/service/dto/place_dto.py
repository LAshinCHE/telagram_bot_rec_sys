from pydantic import BaseModel, Field

class CreatePlaceDTO(BaseModel):
    name: str
    description: str
    city: str
    address_text: str
    price_level: int = Field(ge=1, le=5)