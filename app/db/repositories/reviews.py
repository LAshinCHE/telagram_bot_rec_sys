from app.service.interfaces.repositories.review_repo import ReviewRepositoryI
from sqlalchemy.orm import Session, joinedload
from app.db.models import Review as ReviewModel
from app.domain.entities.review import Review as ReviewEntity
from app.domain.enum import ReviewStatus
from sqlalchemy import select, func

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
    
    def exists_by_user(self, user_id: int, place_id: int) -> bool:
        stmt = select(1).where(ReviewEntity.id == user_id).where(ReviewEntity.place_id == place_id).exists()
        return self.db.scalar(stmt)
    
    def add_review(self, review: ReviewEntity) -> ReviewEntity:
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)

        review = self.session.query(review).filter_by(id=id).first()
        return review

    def get_reviews_for_place(self, place_id: int) -> list[ReviewEntity]:
        pass

    def moderate_review(self, review_id: int, moderator_id: int, status: ReviewStatus) -> ReviewEntity:
        pass

    def get_reviews_for_moderate(self):
        pass

    def get_count_rating_user(self, user_id: int):
        pass


