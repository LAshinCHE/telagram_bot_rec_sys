from dataclasses import dataclass
from datetime import datetime
from app.domain.enum import PlaceStatus

@dataclass
class Place:
    id: int | None
    name: str
    city: str 
    price_level: int
    status: PlaceStatus
    created_by: int
    created_at: datetime

    def approve(self):
        self.status = PlaceStatus.ACTIVE

    def reject(self):
        self.status = PlaceStatus.REJECTED

