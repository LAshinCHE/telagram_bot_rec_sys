from abc import ABC, abstractmethod
from app.domain.entities.place import Place
from app.db.models.place import Place as PlaceModel

class PlaceRepositoryI(ABC):

    @abstractmethod
    def save(self, place: Place) -> int:
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

    @abstractmethod
    def add_tags(self, place_id: int, tags_ids: list[int]) -> PlaceModel:
        pass