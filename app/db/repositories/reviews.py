from app.service.interfaces.repositories.review_repo import ReviewRepositoryI
from sqlalchemy.orm import Session
from app.db.models import Review as ReviewModel
from app.domain.entities.review import Review as ReviewEntity
from app.domain.enum import ReviewStatus

class ReviewRepository(ReviewRepositoryI):
    def __init__(self, session: Session):
        self.session = session

    def get_reviews(self) -> list[ReviewEntity]:
        review_rows = self.session.query(ReviewModel).all()

        reviews = []
        for row in review_rows:
            review = ReviewEntity(
                id=row.id,
                place_id=row.place_id,
                author_id=row.author_id,
                rating=row.rating,
                text=row.text,
                status=ReviewStatus(row.status),
                created_at=row.created_at,
                moderated_by=row.moderated_by,
                moderated_at=row.moderated_at,
                moderation_reason=row.moderation_reason
            )
            reviews.append(review)

        return reviews
