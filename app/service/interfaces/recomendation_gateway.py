from abc import ABC, abstractmethod
from typing import Any

class RecomendationGateway(ABC):

    @abstractmethod
    def get_recomendation(self, euser_id: int, candidates: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def train_model(self, name_model: str):
        pass