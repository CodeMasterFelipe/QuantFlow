class EventHandler:
    def __init__(self, strategy, risk_manager, portfolio, oms, event_queue):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.portfolio = portfolio
        self.oms = oms
        self.event_queue = event_queue
