from quantflow.core.execution_handler import ExecutionHandler
from quantflow.core.events import FillEvent
from quantflow.core.types import Fill


class BacktestExecutionHandler(ExecutionHandler):
    def __init__(self, event_queue, market_data):
        """
        Initializes the backtest execution handler with the event queue and market data

        Args:
            event_queue (EventQueue): The event queue to place FillEvents
            market_data (pd.DataFrame): The data feed to retrieve market prices from
        """
        self.event_queue = event_queue
        self.market_data = market_data

    def execute_order(self, order):
        """
        Simulates the execution of an order in a backtest environment
        Assumes order are filled immediately at the current price from the market data

        Args:
            order (Order): The order to execute
        """
        current_price = self.market_data.loc[order.symbol, "close"]
        fill = Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            fill_price=current_price,
            fill_quantity=order.quantity,
            order_side=order.side,
        )
        fill_event = FillEvent(fill)
        self.event_queue.put(fill_event)
