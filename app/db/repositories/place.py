from app.service.interfaces.repositories.place_repo import PlaceRepository
from domain.entities.place import Place

class PlaceRepository(PlaceRepository):

    def save(self, place: Place) -> Place:
        pass

    def search(self, filters: dict) -> list[Place]:
        pass