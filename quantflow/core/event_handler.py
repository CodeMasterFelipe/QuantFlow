from quantflow.core.events import SignalEvent, OrderRequestEvent


class EventHandler:
    def __init__(self, strategy, risk_manager, portfolio, oms, event_queue):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.portfolio = portfolio
        self.oms = oms
        self.event_queue = event_queue

    def handle_event(self, event):
        new_event = event.process(self)
        if new_event:
            self.event_queue.put(new_event)

    def process_market_event(self, event) -> SignalEvent | None:
        signal = self.strategy.on_new_data(event.data)
        if signal:
            return SignalEvent(signal)

    def process_signal_event(self, event) -> OrderRequestEvent | None:
        order_request = self.risk_manager.generate_order_request(event.data)
        if order_request:
            return OrderRequestEvent(order_request)

    def process_order_request_event(self, event) -> None:
        self.oms.handle_order_request(event.data)

    def process_fill_event(self, event) -> None:
        self.portfolio.update_portfolio(event.data)
