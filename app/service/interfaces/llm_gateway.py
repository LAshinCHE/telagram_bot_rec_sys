from abc import ABC, abstractmethod
from typing import Any

class LLMGateway(ABC):

    @abstractmethod
    def exectue_entities(self, example_query: str):
        pass

    @abstractmethod
    def generate_answer(self, json_recomendations: str) -> dict[str, Any]:
        pass