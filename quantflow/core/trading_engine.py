from quantflow.backtesting import BacktestDataFeed, BacktestExecutionHandler
from quantflow.core import (
    Strategy,
    EventQueue,
    EventHandler,
    DataFeed,
    ExecutionHandler,
    RiskManager,
    SimpleRiskManager,
    Portfolio,
    OrderManagementSystem,
)
from quantflow.core.events import MarketEvent


class TradingEngine:
    def __init__(
        self,
        strategy: Strategy,
        data_feed: DataFeed | None = None,
        execution_handler: ExecutionHandler | None = None,
        risk_manager: RiskManager | None = None,
        historical_data: str | None = None,
    ):
        self.event_queue = EventQueue()
        self.data_feed = data_feed or BacktestDataFeed(historical_data)
        self.portfolio = Portfolio()
        self.strategy = strategy
        self.risk_manager = risk_manager or SimpleRiskManager(self.portfolio)
        self.execution_handler = execution_handler or BacktestExecutionHandler(
            self.event_queue, historical_data
        )
        self.oms = OrderManagementSystem(self.event_queue, self.execution_handler)
        self.event_handler = EventHandler(
            self.strategy, self.risk_manager, self.portfolio, self.oms, self.event_queue
        )

    def run(self):
        data_generator = iter(self.data_feed)
        for data in data_generator:
            market_event = MarketEvent(data)
            self.event_queue.put(market_event)

            # process all events in the queue
            while not self.event_queue.is_empty():
                event = self.event_queue.get()
                if event:
                    self.event_handler.handle_event(event)
