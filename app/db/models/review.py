from sqlalchemy import ForeignKey, Integer, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.database import Base
from app.domain.enum import ReviewStatus


class Rating(Base):
    __tablename__ = "ratings"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"), primary_key=True
    )
    rating: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate = datetime.now,
        )



class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int]
    text: Mapped[str]
    status: Mapped[ReviewStatus]
    moderated_by: Mapped[int | None]
    moderated_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
