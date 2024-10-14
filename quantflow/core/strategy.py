from abc import ABC, abstractmethod
from quantflow.core.types import Signal


class Strategy(ABC):
    """
    Abstract base class for all trading strategies in QuantFlow.

    Subclasses must implement the `on_new_data` method to define your trading logic.
    """

    def __init__(self):
        pass

    @abstractmethod
    def on_new_data(self, data: dict) -> Signal | None:
        """
        This method is called whenever new data is available.

        Args:
            data (dict): The data that is available.

        Returns:
            dict | None: The trading signals that are generated.
        """
        pass
