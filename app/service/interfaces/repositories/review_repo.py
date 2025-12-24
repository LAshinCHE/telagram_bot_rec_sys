from abc import ABC, abstractmethod
from domain.entities.review import Review

class ReviewRepositoryI(ABC):

    @abstractmethod
    def exists_by_user(self, user_id: int, place_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, review: Review) -> Review:
        pass