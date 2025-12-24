
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Float,
    UniqueConstraint,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repositories.database import Base


class RecoModelVersion(Base):
    __tablename__ = "reco_model_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    algo: Mapped[str] = mapped_column(String, nullable=False)
    trained_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    metrics_json: Mapped[dict | None] = mapped_column(JSON)
    artifact_uri: Mapped[str | None]

    recommendations = relationship(
        "UserRecommendation",
        back_populates="model_version",
        cascade="all, delete"
    )


class UserRecommendation(Base):
    __tablename__ = "user_recommendations"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"),
        primary_key=True
    )
    model_version_id: Mapped[int] = mapped_column(
        ForeignKey("reco_model_versions.id", ondelete="CASCADE"),
        primary_key=True
    )

    score: Mapped[float] = mapped_column(Float, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    model_version = relationship(
        "RecoModelVersion",
        back_populates="recommendations"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "place_id",
            "model_version_id",
            name="uq_user_place_model"
        ),
    )
