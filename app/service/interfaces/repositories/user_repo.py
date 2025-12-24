from abc import ABC, abstractmethod
from app.domain.entities.user import User

class UserRepositoryI(ABC):

    @abstractmethod
    def save(self, place: Place) -> Place:
        pass
