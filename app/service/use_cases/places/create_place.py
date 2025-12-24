from datetime import datetime
from domain.entities.place import Place
from domain.enum import PlaceStatus

class CreatePlaceUseCase:

    def __init__(self, place_repo):
        self.place_repo = place_repo

    def execute(self, dto, user):
        place = Place(
            id=None, 
            name=dto.name,
            description=dto.description, 
            city=dto.city,
            address_text=dto.address_text,
            price_level=dto.price_level,
            status=PlaceStatus.PENDING,
            created_by=user.id,
            created_at=datetime.now()
        )
        return self.place_repo.save(place)