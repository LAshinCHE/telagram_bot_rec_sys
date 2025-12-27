from app.db.models.user import User, UserRole
from app.db.repositories.user import UserRepository
from app.domain.entities.user import User as UserEntity

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> UserEntity:
        return self.user_repo.get(user_id)

    def create_user(self, user_id: int, name: str, role: UserRole) -> UserEntity:
        return self.user_repo.add(
            id=user_id,
            name=name,
            role=role,
        )
