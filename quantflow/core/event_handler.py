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
