from app.service.interfaces.repositories.review_repo import ReviewRepositoryI
from domain.entities.review import Review

class ReviewRepository(ReviewRepositoryI):

    def get_reviews(self) -> list[Review]:
        pass
