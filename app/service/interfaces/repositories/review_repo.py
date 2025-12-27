from abc import ABC, abstractmethod
from app.domain.entities.review import Review

class ReviewRepositoryI(ABC):

    @abstractmethod
    def get_reviews(self) -> list[Review]:
        pass

    @abstractmethod
    def add_review(self, review: Review) -> Review:
        pass

    # @abstractmethod
    # def get_reviews_for_place(self, place_id: int) -> list[Review]:
    #     pass

    # @abstractmethod
    # def moderate_review(self, review_id: int, moderator_id: int, status: Review) -> Review:
    #     pass

    # @abstractmethod
    # def get_reviews_for_moderate(self):
    #     pass

    # @abstractmethod
    # def get_count_rating_user(self, user_id: int):
    #     pass

    @abstractmethod
    def exists_by_user(self, user_id: int, place_id: int) -> bool:
        pass