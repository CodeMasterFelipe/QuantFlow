from abc import ABC, abstractmethod
from typing import Generator


class DataFeed(ABC):
    @abstractmethod
    def __iter__(self) -> Generator:
        pass
