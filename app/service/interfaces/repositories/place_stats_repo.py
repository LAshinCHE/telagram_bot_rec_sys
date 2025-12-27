from abc import ABC, abstractmethod
from app.domain.entities.place import Place

class PlaceStatsRepositoryI(ABC):
    
    @abstractmethod
    def update_after_review(self, place_id: int):
        pass