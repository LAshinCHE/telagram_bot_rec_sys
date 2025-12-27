from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, func
from app.db.models import Place as PlaceModel
from app.db.models.place import Place, PlaceStats, Tag
from app.domain.entities.place import Place as PlaceEntity


class PlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_places(
        self,
        city: str | None = None,
        price_level: int | None = None,
        include_tags: list[str] | None = None,
        status: str = "active",
    ) -> list[dict]:
        """
        Поиск мест по фильтрам.
        include_tags — обязательные теги (AND логика)
        """

        stmt = (
            select(Place)
            .options(
                selectinload(Place.tags),
                selectinload(Place.stats),
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
                .join(Place.tags)
                .where(Tag.name.in_(include_tags))
                .group_by(Place.id)
                .having(func.count(func.distinct(Tag.id)) == len(include_tags))
            )

        places = self.db.execute(stmt).scalars().all()

        result: list[dict] = []

        for place in places:
            stats = place.stats

            result.append(
                {
                    "id": place.id,
                    "name": place.name,
                    "description": place.description,
                    "city": place.city,
                    "address_text": place.address_text,
                    "price_level": place.price_level,
                    "status": place.status,
                    "created_at": place.created_at,
                    "updated_at": place.updated_at,
                    "tags": [tag.name for tag in place.tags],
                    "stats": {
                        "rating_avg": stats.rating_avg if stats else None,
                        "rating_cnt": stats.rating_cnt if stats else 0,
                        "reviews_cnt": stats.reviews_cnt if stats else 0,
                        "updated_at": stats.updated_at if stats else None,
                    },
                }
            )

        return result

    
    def search(self, filters: dict) -> list[Place]:
        return self.__search_places(
            city=filters.get("city"),
            price_level=filters.get("price_level"),
            include_tags=filters.get("selected_tags")
        )
    
    def get_by_id(self, place_id: int) -> Place:
        return self.db.query(Place).filter_by(id=place_id).first()
    
    def add_tags(self, place_id: int, tags_ids: list[int]) -> Place:
        place = self.db.get(Place, place_id)

        if not tags_ids:
            return place

        # Получаем существующие теги
        tags = (
            self.db.execute(
                select(Tag).where(Tag.id.in_(tags_ids))
            )
            .scalars()
            .all()
        )

        # Добавляем только те теги, которых ещё нет у места
        existing_tag_ids = {tag.id for tag in place.tags}

        for tag in tags:
            if tag.id not in existing_tag_ids:
                place.tags.append(tag)

        self.db.add(place)
        self.db.commit()
        self.db.refresh(place)

        return place
