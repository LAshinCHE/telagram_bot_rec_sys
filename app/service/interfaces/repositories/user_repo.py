from abc import ABC, abstractmethod
from app.domain.entities.user import User
from app.domain.enum import UserRole

class UserRepositoryI(ABC):
    
    @abstractmethod
    def add(self, id: int, name: str, role: UserRole) -> User:
        pass

    @abstractmethod
    def get(self, id: int) -> User:
        pass
