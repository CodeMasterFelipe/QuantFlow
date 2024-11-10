from abc import ABC, abstractmethod
from quantflow.core.types import Fill


class ExecutionHandler(ABC):
    @abstractmethod
    def execute_order(self, order) -> Fill:
        """
        Execute and order. This method should be implemented by concrete subclasses for backtesting or live trading.
        """
        pass
