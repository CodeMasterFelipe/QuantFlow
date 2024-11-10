from quantflow.core.events import FillEvent
from quantflow.core.types import SignalType
from quantflow.core.shared_context import SharedContext


class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 0.0
        self.shared_context = SharedContext()

    def update_portfolio(self, fill: Fill):
        symbol = fill.symbol
        if symbol not in self.positions:
            self.positions[symbol] = 0

        if fill.order_side == OrderSide.BUY:
            self.cash -= fill.fill_price * fill.fill_quantity
            self.positions[symbol] += fill.fill_quantity
        elif fill.order_side == OrderSide.SELL:
            self.cash += fill.fill_price * fill.fill_quantity
            self.positions[symbol] -= fill.fill_quantity

    def get_position(self, symbol):
        return self.positions.get(symbol, 0)

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
