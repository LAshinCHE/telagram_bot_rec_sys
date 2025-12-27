from app.service.interfaces.repositories.user_repo import UserRepositoryI
from sqlalchemy.orm import Session
from app.db.models import User as UserModel
from app.domain.entities.user import User as UserEntity
from app.domain.enum import UserRole
import datetime

class UserRepository(UserRepositoryI):
    def __init__(self, session: Session):
        self.session = session

    def add(self, id: int, name: str, role: UserRole) -> UserEntity:
        user_model = UserModel(
            id=id,
            name=name,
            role=role,
            created_at=datetime.datetime.utcnow(),
        )

        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            role=user_model.role,
            created_at=user_model.created_at,
        )

    def get(self, id: int) -> UserEntity | None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()
        if not user_model:
            return None

        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            role=user_model.role,
            created_at=user_model.created_at,
        )
