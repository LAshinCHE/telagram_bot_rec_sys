from abc import ABC, abstractmethod
from typing import Any

class RecommendationGateway(ABC):

    @abstractmethod
    def get_recommendation(self, euser_id: int, candidates: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def train_model(self, name_model: str):
        pass