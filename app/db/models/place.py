from sqlalchemy import String, ForeignKey, Integer, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    city: Mapped[str]
    address_text: Mapped[str | None]
    price_level: Mapped[int | None]
    status: Mapped[str]  # pending|active|rejected|archived
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=text("TIMEZOEN('utc', now())"))
    updated_at: Mapped[datetime | None] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate = datetime.now,
        )

    tags = relationship("Tag", secondary="place_tags", back_populates="places")
    stats = relationship("PlaceStats", uselist=False)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    places = relationship("Place", secondary="place_tags", back_populates="tags")


class PlaceTag(Base):
    __tablename__ = "place_tags"

    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    
class PlaceStats(Base):
    __tablename__ = "place_stats"

    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"), primary_key=True
    )
    rating_avg: Mapped[float | None]
    rating_cnt: Mapped[int]
    reviews_cnt: Mapped[int]
    updated_at: Mapped[datetime]