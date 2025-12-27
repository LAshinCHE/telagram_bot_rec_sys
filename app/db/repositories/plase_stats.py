from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.db.models.place import PlaceStats, Place
from app.db.models.review import Review

class PlaceStatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def update_after_review(self, place_id: int):
        stmt = select(
            func.count(Review.id),
            func.avg(Review.rating)
        ).where(Review.place_id == place_id)
    
        review_count, avg_rating = self.db.execute(stmt).tuple()
        avg_rating = float(avg_rating or 0)

        stats_stmt = select(PlaceStats).where(PlaceStats.place_id == place_id)
        place_stats = self.db.execute(stats_stmt).scalar_one_or_none()

        if place_stats:
            place_stats.review_count = review_count
            place_stats.avg_rating = avg_rating
        else:
            place_stats = PlaceStats(
                place_id=place_id,
                review_count=review_count,
                avg_rating=avg_rating
            )
            self.db.add(place_stats)


        self.db.commit()