from quantflow.core.events import FillEvent
from quantflow.core.types import SignalType
from quantflow.core.shared_context import SharedContext


class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 0.0
        self.shared_context = SharedContext()

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
        latest_price = self.shared_context.get_latest_price()
        total_equity = self.cash
        for symbol, position in self.positions.items():
            total_equity += position * latest_price[symbol]
        return total_equity

    def __str__(self):
        return f"Portfolio(cash={self.cash}, positions={self.positions})"

    def __repr__(self):
        return self.__str__()
