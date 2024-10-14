from abc import ABC, abstractmethod


class ExecutionHandler(ABC):
    @abstractmethod
    def execute_order(self, order):
        """
        Execute and order. This method should be implemented by concrete subclasses for backtesting or live trading.
        """
        pass
