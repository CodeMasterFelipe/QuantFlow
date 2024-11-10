from quantflow.core.events import FillEvent
from quantflow.core.types import Fill, OrderSide, SignalType
from quantflow.core.shared_context import SharedContext
import logging


class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 0.0
        self.shared_context = SharedContext()
        self.good_trades = 0
        self.bad_trades = 0

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
        
        if "takeprofit" in fill.order_id:
            self.good_trades += 1
            logging.info(f"Good trade: {self}")
        elif "stoploss" in fill.order_id:
            self.bad_trades += 1
            logging.info(f"Bad trade: {self}")
        
        logging.info(f"Portfolio updated: {self}")

    def get_position(self, symbol):
        return self.positions.get(symbol, 0)

    def get_equity(self):
        latest_price = self.shared_context.get_latest_price()
        total_equity = self.cash
        for _, position in self.positions.items():
            total_equity += position * latest_price
        return total_equity
    
    def get_accuracy(self):
        return self.good_trades / (self.good_trades + self.bad_trades)

    def __str__(self):
        return f"Portfolio(cash={self.cash}, positions={self.positions})"

    def __repr__(self):
        return self.__str__()
