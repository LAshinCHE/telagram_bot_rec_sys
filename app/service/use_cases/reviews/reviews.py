
from app.domain.entities.review import Review
from app.domain.enum import ReviewStatus
from app.exceptions.exceptions import BusinessError
from datetime import datetime
from app.db.repositories.reviews import ReviewRepository
from app.db.repositories.place import PlaceRepository
from app.db.repositories.plase_stats import PlaceStatsRepository

class ReviewService:

    def __init__(
        self,
        review_repo: ReviewRepository,
        place_repo: PlaceRepository,
        place_stats_repo: PlaceStatsRepository
    ):
        self.review_repo = review_repo
        self.place_repo = place_repo
        self.place_stats_repo = place_stats_repo

    def add_review(self, dto, user):
        # Check place
        if not self.place_repo.exists_active(dto.place_id):
            raise BusinessError("Place not found or inactive")

        if self.review_repo.exists_by_user(user.id, dto.place_id):
            raise BusinessError("Review already exists")

        status = (
            ReviewStatus.APPROVED
            if user.role in ("moderator", "admin")
            else ReviewStatus.PENDING
        )

        review = Review(
            id=None,
            place_id=dto.place_id,
            author_id=user.id,
            rating=dto.rating,
            text=dto.text,
            status=status,
            created_at=datetime.utcnow()
        )

        review = self.review_repo.add_review(review)

        if review.status == ReviewStatus.APPROVED:
            self.place_stats_repo.update_after_review(dto.place_id)

        return review
