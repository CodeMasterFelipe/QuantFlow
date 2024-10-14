from abc import ABC, abstractmethod
from quantflow.core.types import OrderRequest, OrderType, Signal


class RiskManager(ABC):
    def __init__(self, portfolio):
        self.portfolio = portfolio

    @abstractmethod
    def generate_order_request(self, signal: Signal) -> OrderRequest | None:
        pass


class SimpleRiskManager(RiskManager):
    def __init__(self, portfolio, risk_per_trade=0.02):
        super().__init__(portfolio)
        self.risk_per_trade = risk_per_trade

    def generate_order_request(self, signal: Signal) -> OrderRequest | None:
        quantity = self.calculate_order_quantity(signal)
        if quantity <= 0:
            return None

        return OrderRequest(
            symbol=signal.symbol,
            quantity=quantity,
            order_type=OrderType.MARKET,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
        )

    def calculate_order_quantity(self, signal: Signal) -> int:
        equity = self.portfolio.get_equity()
        risk_amount = equity * self.risk_per_trade

        stop_loss_price = signal.stop_loss
        current_price = signal.current_price

        if stop_loss_price:
            price_diff = abs(current_price - stop_loss_price)
            if price_diff == 0:
                return 0
            return int(risk_amount / price_diff)
        else:
            return int(risk_amount / current_price)
