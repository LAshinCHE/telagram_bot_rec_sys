from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.db.models.place import Place, PlaceStats, Tag


class PlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_places(
        self,
        city: str | None = None,
        price_level: int | None = None,
        include_tags: list[str] | None = None,
        status: str = "active",
    ) -> list[Place]:
        """
        Поиск мест по фильтрам.
        include_tags — обязательные теги (AND логика)
        """

        stmt = (
            select(Place)
            .join(Place.tags)
            .outerjoin(PlaceStats)
            .options(
                joinedload(Place.tags),
                joinedload(Place.stats),
            )
            .where(Place.status == status)
        )

        if city:
            stmt = stmt.where(Place.city == city)

        if price_level is not None:
            stmt = stmt.where(Place.price_level == price_level)

        if include_tags:
            stmt = (
                stmt
                .where(Tag.name.in_(include_tags))
                .group_by(Place.id, PlaceStats.rating_avg)
                .having(func.count(func.distinct(Tag.id)) == len(include_tags))
            )
        else:
            stmt = stmt.group_by(Place.id, PlaceStats.rating_avg)

        return self.db.scalars(stmt).all()
