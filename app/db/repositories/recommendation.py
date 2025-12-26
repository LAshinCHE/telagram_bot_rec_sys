from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.db.models.place import Place, PlaceStats, Tag


class RecommendatioRepository:
    def __init__(self, db: Session):
        self.db = db