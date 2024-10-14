from quantflow.core.events import FillEvent
from quantflow.core.types import SignalType


class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 0.0
        self.event_queue = None

    def update_portfolio(self, fill: FillEvent):
        symbol = fill.data.symbol
        if symbol not in self.positions:
            self.positions[symbol] = 0

        if fill.data.order_side == SignalType.BUY:
            self.cash -= fill.data.fill_price * fill.data.fill_quantity
            self.positions[symbol] += fill.data.fill_quantity
        elif fill.data.order_side == SignalType.SELL:
            self.cash += fill.data.fill_price * fill.data.fill_quantity
            self.positions[symbol] -= fill.data.fill_quantity

    def get_position(self, symbol):
        return self.positions.get(symbol, [])

    def get_equity(self):
        return self.cash

    def __str__(self):
        return f"Portfolio(cash={self.cash}, positions={self.positions})"

    def __repr__(self):
        return self.__str__()
