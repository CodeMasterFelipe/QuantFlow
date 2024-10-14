from dataclasses import dataclass
@dataclass
class Fill:
    order_id: str
    symbol: str
    fill_price: float
    fill_quantity: int
    order_side: SignalType
    order_type: OrderType = OrderType.MARKET
