from app.exceptions import NotFound
from app.service.interfaces.repositories.place_repo import PlaceRepositoryI
from app.domain.entities.place import Place

class GetPlaceUseCase:

    def __init__(self, place_repo : PlaceRepositoryI):
        self.place_repo = place_repo

    def execute(self, place_id: int) -> Place:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise NotFound("Place not found")
        return place
