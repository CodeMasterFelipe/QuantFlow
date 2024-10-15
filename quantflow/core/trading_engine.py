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
    """
    The TradingEngine class is responsible for coordinnating all the components of the trading system.
    It can be use for both backtesting and live trading.

    Attributes:
        event_queue (EventQueue): The queue that stores all the events.
        data_feed (DataFeed): The data feed that provides the data, either backtest data or live data.
        portfolio (Portfolio): The portfolio that stores the account information.
        strategy (Strategy): The strategy that generates signals.
        risk_manager (RiskManager): The risk manager that manages the risk.
        execution_handler (ExecutionHandler): Execute order in the market, backtest or live.
        oms (OrderManagementSystem): Manages the lifecycle of the orders.
        event_handler (EventHandler): Process the events and coordinates interaction between the components.

    Usage:
        engine = TradingEngine(MovingAverageStrategy(), historical_data="data.csv")
        engine.run()
    """

    def __init__(
        self,
        strategy: Strategy,
        data_feed: DataFeed | None = None,
        execution_handler: ExecutionHandler | None = None,
        risk_manager: RiskManager | None = None,
        historical_data: str | None = None,
    ):
        """
        Initialize the TradingEngine with the specified strategy and components.

        Args:
            strategy (Strategy): The strategy that generates signals.
            data_feed (DataFeed): The data feed that provides the data, either backtest data or live data.
            execution_handler (ExecutionHandler): Execute order in the market, backtest or live.
            risk_manager (RiskManager): The risk manager that manages the risk.
            historical_data (str): The path to the historical data file.
        """
        self.event_queue = EventQueue()
        self.data_feed = data_feed or BacktestDataFeed(historical_data)
        self.portfolio = Portfolio()
        self.strategy = strategy
        self.risk_manager = risk_manager or SimpleRiskManager(self.portfolio)
        self.execution_handler = execution_handler or BacktestExecutionHandler(
            self.event_queue
        )
        self.oms = OrderManagementSystem(self.event_queue, self.execution_handler)
        self.event_handler = EventHandler(
            self.strategy, self.risk_manager, self.portfolio, self.oms, self.event_queue
        )

    def run(self):
        """
        Start the trading engine, process data and event in a loop until data feed is exhausted.
        """
        data_generator = iter(self.data_feed)
        for data in data_generator:
            market_event = MarketEvent(data)
            self.event_queue.put(market_event)

            # process all events in the queue
            while not self.event_queue.is_empty():
                event = self.event_queue.get()
                if event:
                    self.event_handler.handle_event(event)
