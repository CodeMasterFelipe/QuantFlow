from quantflow.core.execution_handler import ExecutionHandler
from quantflow.core.events import FillEvent
from quantflow.core.types import Fill, OrderSide
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

    def execute_order(self, order) -> Fill:
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
            fill_price=order.price,
            fill_quantity=order.quantity,
            order_side=order.side,
        )
        self.shared_context.add_stoploss_takeprofit_order(order.symbol, stoploss=order.stop_loss, takeprofit=order.take_profit, quantity=order.quantity)

        return fill
    
    def check_stoploss_takeprofit(self):
        """check if stoploss or takeprofit is hit if so, send back a fill signal which should update the portfolio later.
        """
        current_price = self.shared_context.latest_price

        
        for order in self.shared_context.get_stoploss_takeprofit_orders():
            if current_price['Low'] <= order["stoploss"]:
                fill = Fill(
                    order_id="stoploss",
                    symbol=order["symbol"],
                    # fill_price=current_price,
                    fill_price=order['stoploss'],
                    # fill_price=current_price['Close'],
                    fill_quantity=order["quantity"],
                    order_side=OrderSide.SELL
                )
                self.event_queue.put(FillEvent(fill))
                self.shared_context.remove_stoploss_takeprofit_order(order)
            elif current_price['High'] >= order["takeprofit"]:
                fill = Fill(
                    order_id="takeprofit",
                    symbol=order["symbol"],
                    # fill_price=current_price,
                    fill_price=order['takeprofit'],
                    fill_quantity=order["quantity"],
                    order_side=OrderSide.SELL
                )
                self.event_queue.put(FillEvent(fill))
                self.shared_context.remove_stoploss_takeprofit_order(order)
