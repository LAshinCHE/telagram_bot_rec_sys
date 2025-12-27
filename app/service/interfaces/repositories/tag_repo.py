from abc import ABC, abstractmethod
from app.domain.entities.tag import Tag as TagEntity

class TagRepositoryI(ABC):

    @abstractmethod
    def fill(self, names: list[str]):
        pass

    @abstractmethod
    def get_all(self) -> list[TagEntity]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> TagEntity:
        pass

    @abstractmethod
    def get_by_id(seld, id: int) -> TagEntity:
        pass
