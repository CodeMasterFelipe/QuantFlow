from quantflow.core.execution_handler import ExecutionHandler
from quantflow.core.events import FillEvent
from quantflow.core.types import Fill
from quantflow.core.shared_context import SharedContext


class BacktestExecutionHandler(ExecutionHandler):
    def __init__(self, event_queue):
        """
        Initializes the backtest execution handler with the event queue and market data

        Args:
            event_queue (EventQueue): The event queue to place FillEvents
            market_data (pd.DataFrame): The data feed to retrieve market prices from
        """
        self.event_queue = event_queue
        self.shared_context = SharedContext()

    def execute_order(self, order):
        """
        Simulates the execution of an order in a backtest environment
        Assumes order are filled immediately at the current price from the market data

        Args:
            order (Order): The order to execute
        """
        current_price = self.shared_context.get_latest_price()
        fill = Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            fill_price=current_price,
            fill_quantity=order.quantity,
            order_side=order.side,
        )
        fill_event = FillEvent(fill)
        self.event_queue.put(fill_event)
