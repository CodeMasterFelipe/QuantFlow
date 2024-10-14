# QuantFlow

QuantFlow is a flexible and robust Python framework for developing, backtesting, and executing quantitative trading strategies. Designed with modularity and scalability in mind, QuantFlow allows you to seamlessly transition between backtesting and live trading environments with minimal code changes. It leverages an event-driven architecture to facilitate clear data flow and decoupled components, making it easier to build, test, and deploy trading algorithms.

### Table of Contents

    • [Features](#features)
    • Installation
    • Quick Start
        • Basic Setup
        • Writing a Strategy
        • Running a Backtest
    • Architecture Overview
        • Components
            • Data Feed
            • Strategy
            • Risk Manager
            • Portfolio
            • Order Management System (OMS)
            • Execution Handler
            • Event Queue
            • Trading Engine
    • Extending QuantFlow
    • Contributing
    • License
    • Contact

## Features

    • Event-Driven Architecture: Facilitates a clear and modular design, enabling components to interact through events.
    • Modularity and Encapsulation: Components are decoupled, making it easy to maintain and extend the framework.
    • Seamless Transition Between Backtesting and Live Trading: Swap out data feeds and execution handlers to switch environments without changing your strategy code.
    • Risk Management: Includes support for stop-loss, take-profit, and dynamic position sizing.
    • User-Friendly Interface: Write your own strategies by subclassing and implementing a few methods.
    • Portfolio Management: Tracks positions, cash balance, and calculates portfolio metrics.
    • Extensible Components: Customize or replace any component to suit your specific needs.

## Installation

QuantFlow requires Python 3.7 or higher. You can install QuantFlow via pip:

pip install quantflow

Note: As QuantFlow is currently under development, you might need to clone the repository and install it manually.

## Quick Start

### Basic Setup

Before diving into writing strategies, let’s set up a basic environment:

```python
from quantflow.core import (
EventQueue,
TradingEngine,
BacktestDataFeed,
BacktestExecutionHandler,
EventHandler,
Portfolio,
Strategy,
RiskManager,
OrderManagementSystem,
)

# Load your historical data

historical_data = load_data('historical_prices.csv')
```

### Writing a Strategy

Create a strategy by subclassing the Strategy class and implementing the on_new_data method:

```python
class MovingAverageStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        self.prices = []
        self.short_window = short_window
        self.long_window = long_window

    def on_new_data(self, data):
        self.prices.append(data['close'])
        if len(self.prices) >= self.long_window:
            short_ma = sum(self.prices[-self.short_window:]) / self.short_window
            long_ma = sum(self.prices[-self.long_window:]) / self.long_window
            symbol = data['symbol']
            current_price = data['close']
            if short_ma > long_ma:
                return Signal(
                    symbol=symbol,
                    signal_type=SignalType.BUY,
                    current_price=current_price,
                    stop_loss=current_price * 0.98,  # 2% stop-loss
                    take_profit=current_price * 1.05  # 5% take-profit
                )
            elif short_ma < long_ma:
                return Signal(
                    symbol=symbol,
                    signal_type=SignalType.SELL,
                    current_price=current_price,
                    stop_loss=current_price * 1.02,
                    take_profit=current_price * 0.95
                )
        return None
```

### Running a Backtest

Set up the necessary components and run the trading engine:

```python
# Initialize components

event_queue = EventQueue()
data_feed = BacktestDataFeed(historical_data)
portfolio = Portfolio()
strategy = MovingAverageStrategy()
risk_manager = RiskManager(portfolio)
execution_handler = BacktestExecutionHandler(event_queue)
oms = OrderManagementSystem(event_queue, execution_handler)
event_handler = EventHandler(strategy, risk_manager, portfolio, oms, event_queue)

# Run the trading engine

engine = TradingEngine(data_feed, event_handler, event_queue)
engine.run()

# Output portfolio performance

print(f"Final Portfolio Equity: {portfolio.get_equity()}")
print(f"Positions: {portfolio.positions}")
```

### Architecture Overview

QuantFlow’s architecture is designed to be modular and extensible, allowing you to customize or replace components as needed.

#### Components

Data Feed

    • Role: Provides market data to the system.
    • BacktestDataFeed: Feeds historical data for backtesting.
    • LiveDataFeed: Connects to live data sources for real-time trading.

Strategy

    • Role: Generates trading signals based on market data.
    • Implementation: Subclass the Strategy class and implement the on_new_data method.

Risk Manager

    • Role: Determines whether to act on signals, considering portfolio state and risk management rules.
    • Implementation: Subclass the RiskManager class and implement the generate_order_request method.

Portfolio

    • Role: Manages positions, cash balance, and calculates portfolio metrics.
    • Responsibilities:
    • Updating positions based on fills.
    • Calculating equity, P&L, and exposure.
    • Providing portfolio information to other components.

Order Management System (OMS)

    • Role: Manages the lifecycle of orders.
    • Responsibilities:
    • Handling order requests from the Risk Manager.
    • Tracking order statuses.
    • Communicating with the Execution Handler.
    • Receiving fills and passing them to the Portfolio.

Execution Handler

    • Role: Executes orders in the market.
    • BacktestExecutionHandler: Simulates order execution for backtesting.
    • LiveExecutionHandler: Interfaces with broker APIs for live trading.

Event Queue

    • Role: Manages events within the system.
    • Implementation: Uses a queue to process events in an orderly fashion.

Trading Engine

    • Role: Coordinates all components and runs the main event loop.
    • Responsibilities:
    • Fetching data from the Data Feed.
    • Placing events into the Event Queue.
    • Processing events through the Event Handler.

## Extending QuantFlow

QuantFlow is designed to be extensible. You can customize or extend its components to suit your needs:

    • Custom Strategies: Implement your own strategies by subclassing Strategy.
    • Advanced Risk Management: Create sophisticated risk managers by subclassing RiskManager.
    • Custom Execution Logic: Develop new execution handlers to implement different execution algorithms.
    • Data Sources: Integrate new data feeds for different markets or data types.
