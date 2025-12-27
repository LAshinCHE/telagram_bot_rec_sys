from abc import ABC, abstractmethod
from app.domain.entities.place import Place

class PlaceRepositoryI(ABC):

    @abstractmethod
    def save(self, place: Place) -> Place:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Place:
        pass

    @abstractmethod
    def search(self, filters: dict) -> list[Place]:
        pass

    @abstractmethod
    def exists_active(self, place_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, place_id: int) -> Place:
        pass