from dataclasses import dataclass
from datetime import datetime
from app.domain.enum import PlaceStatus

@dataclass
class Place:
    id: int | None
    name: str
    description: str
    city: str 
    address_text: str
    price_level: int
    status: PlaceStatus | None
    created_by: int
    created_at: datetime | None

    def approve(self):
        self.status = PlaceStatus.ACTIVE

    def reject(self):
        self.status = PlaceStatus.REJECTED

