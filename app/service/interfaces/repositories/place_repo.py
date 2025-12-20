from abc import ABC, abstractmethod
from domain.entities.review import Review

class PlaceRepository(ABC):

    @abstractmethod
    def exists_active(self, place_id: int) -> bool:
        pass