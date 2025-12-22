from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.repositories import Base


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
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime | None]

    tags = relationship("Tag", secondary="place_tags", back_populates="places")
    photos = relationship("PlacePhoto", cascade="all, delete")
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


class PlacePhoto(Base):
    __tablename__ = "place_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id", ondelete="CASCADE"))
    url: Mapped[str]
    uploaded_by: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
