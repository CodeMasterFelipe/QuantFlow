from abc import ABC, abstractmethod
from quantflow.core.types import OrderRequest, OrderType, Signal


class RiskManager(ABC):
    def __init__(self, portfolio):
        self.portfolio = portfolio

    @abstractmethod
    def generate_order_request(self, signal: Signal) -> OrderRequest | None:
        pass

