from abc import ABC, abstractmethod
from typing import Dict, Any


Config = Dict[str, Any]

Strategy = Dict[str, Dict[str, str]]


class Factory(ABC):
    @abstractmethod
    def __init__(self, config: Config) -> None:
        """Factory constructor to be implemented"""

    def extract(self, method: str):
        return getattr(self, "{0}".format(method), None)
