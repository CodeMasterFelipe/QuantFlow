from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class Signal:
    symbol: str
    signal_type: SignalType
    current_price: float
    stop_loss: float | None = None
    take_profit: float | None = None
    quantity: float | None = None


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


@dataclass
class OrderRequest:
    symbol: str
    quantity: int
    order_type: OrderType
    stop_loss: float | None = None
    take_profit: float | None = None


class OrderStatus(Enum):
    NEW = "NEW"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


@dataclass
class Order:
    order_id: str
    symbol: str
    order_type: OrderType
    quantity: int
    stop_loss: float | None = None
    take_profit: float | None = None
    status: OrderStatus = OrderStatus.NEW


@dataclass
class Fill:
    order_id: str
    symbol: str
    fill_price: float
    fill_quantity: int
    order_side: SignalType
    order_type: OrderType = OrderType.MARKET
