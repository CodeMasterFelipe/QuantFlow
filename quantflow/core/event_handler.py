from quantflow.core.events import SignalEvent, OrderRequestEvent, FillEvent
from quantflow.core.shared_context import SharedContext
import logging


class EventHandler:
    def __init__(self, strategy, risk_manager, portfolio, oms, event_queue):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.portfolio = portfolio
        self.oms = oms
        self.event_queue = event_queue
        self.shared_context = SharedContext()

    def handle_event(self, event):
        new_event = event.process(self)
        if new_event:
            self.event_queue.put(new_event)

    def process_market_event(self, event) -> SignalEvent | None:
        signal = self.strategy.on_new_data(event.data)
        self.shared_context.update_latest_price(event.data)
        self.check_stoploss_takeprofit()
        if signal:
            return SignalEvent(signal)

    def process_signal_event(self, event) -> OrderRequestEvent | None:
        order_request = self.risk_manager.generate_order_request(event.data)
        logging.info(f"Order request: {order_request}")
        if order_request:
            return OrderRequestEvent(order_request)

    def process_order_request_event(self, event) -> FillEvent | None:
        fill = self.oms.handle_order_request(event.data)
        logging.info(f"Fill: {fill}")
        if fill:
            return FillEvent(fill)

    def process_fill_event(self, event) -> None:
        logging.info(f"Updating portfolio with: {event.data}")
        self.portfolio.update_portfolio(event.data)

    def check_stoploss_takeprofit(self):
        """check if stoploss or takeprofit is hit if so, send back a fill signal which should update the portfolio later.
        """
        self.oms.check_stoploss_takeprofit()