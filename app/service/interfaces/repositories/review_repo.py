from abc import ABC, abstractmethod
from app.domain.entities.review import Review

class ReviewRepositoryI(ABC):

    @abstractmethod
    def exists_by_user(self, user_id: int, place_id: int) -> bool:
        pass

    @abstractmethod
    def get_reviews(self) -> list[Review]:
        pass