from abc import ABC, abstractmethod
from app.domain.entities.review import Review

class ReviewRepositoryI(ABC):

    @abstractmethod
    def get_reviews(self) -> list[Review]:
        pass