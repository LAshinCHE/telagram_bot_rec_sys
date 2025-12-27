from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.db.models import Place as PlaceModel
from app.db.models.place import Place, PlaceStats, Tag
from app.domain.entities.place import Place as PlaceEntity


class PlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def __search_places(
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

        stmt = select(Place).outerjoin(Place.stats).where(Place.status == status)

        if city:
            stmt = stmt.where(Place.city == city)
        if price_level is not None:
            stmt = stmt.where(Place.price_level == price_level)

        if include_tags:
            # Логика AND для тегов
            stmt = (
                stmt.join(Place.tags)
                .where(Tag.name.in_(include_tags))
                .group_by(Place.id)
                .having(func.count(func.distinct(Tag.id)) == len(include_tags))
            )
        

        stmt = stmt.options(joinedload(Place.tags), joinedload(Place.stats))


        return self.db.scalars(stmt).unique().all()
    

    def exists_active(
            self,
            place_id: int
    ) -> bool:
        return self.db.scalar(select(select(Place.id).where(Place.id == place_id).exists()))
    

    def save(self, place: PlaceEntity) -> int:
        place_model = PlaceModel(
            name=place.name,
            description=place.description,
            city=place.city,
            address_text=place.address_text,
            price_level=place.price_level,
            status=place.status.value if place.status else "pending",
            created_by=place.created_by,
            created_at=place.created_at,
        )

        self.db.add(place_model)
        self.db.commit()
        self.db.refresh(place_model)

        return place_model.id
    
    def search(self, filters: dict) -> list[Place]:
        return self.__search_places(
            city=filters.get("city"),
            price_level=filters.get("price_level"),
            include_tags=filters.get("selected_tags")
        )
    
    def get_by_id(self, place_id: int) -> Place:
        return self.db.query(Place).filter_by(id=place_id).first()
