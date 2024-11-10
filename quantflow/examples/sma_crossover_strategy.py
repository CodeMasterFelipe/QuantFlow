import argparse
from quantflow.core.types import Signal, SignalType
from quantflow.backtesting import BacktestDataFeed

# from quantflow.core import Strategy, TradingEngine
from quantflow.core.strategy import Strategy
from quantflow.core.trading_engine import TradingEngine

import logging


class SMACrossoverStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []
        self.prev_short_ma = -1
        self.prev_long_ma = -1

    def on_new_data(self, data) -> Signal | None:
        current_price = data["Close"]
        self.prices.append(current_price)

        if len(self.prices) < self.long_window:
            return

        short_ma = sum(self.prices[-self.short_window :]) / self.short_window
        long_ma = sum(self.prices[-self.long_window :]) / self.long_window

        signal = self._detect_crossover(
            data["Symbol"], current_price, short_ma, long_ma
        )

        self.prev_short_ma = short_ma
        self.prev_long_ma = long_ma
        return signal

    def _detect_crossover(self, symbol, current_price, short_ma, long_ma):
        if self._bullish_crossover(short_ma, long_ma):
            return Signal(
                symbol=symbol,
                signal_type=SignalType.BUY,
                current_price=current_price,
                stop_loss=current_price * 0.99,
                take_profit=current_price * 1.02,
            )
        if self._bearish_crossover(short_ma, long_ma):
            pass
            # return Signal(
            #     symbol=symbol,
            #     signal_type=SignalType.SELL,
            #     current_price=current_price,
            #     stop_loss=current_price * 1.01,
            #     take_profit=current_price * 0.98,
            # )
        return None

    def _bullish_crossover(self, short_ma, long_ma):
        return self.prev_short_ma < self.prev_long_ma and short_ma > long_ma

    def _bearish_crossover(self, short_ma, long_ma):
        return self.prev_short_ma > self.prev_long_ma and short_ma < long_ma


def run_strategy(data_path: str, resample_period: str | None = None):
    backtest_data_feed = BacktestDataFeed(data_path, datetime_col="Timestamp")
    if resample_period:
        backtest_data_feed.resample(resample_period)

    engine = TradingEngine(SMACrossoverStrategy(short_window=50, long_window=200), data_feed=backtest_data_feed)
    engine.portfolio.cash = 10_000
    engine.run()

    print(f"Final portfolio equity: {engine.portfolio.get_equity()}")
    print(f"Positions: {engine.portfolio.positions}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SMA Crossover Strategy")
    parser.add_argument("data_path", type=str, help="Path to the historical data file")
    parser.add_argument(
        "--resample_period", type=str, help="Resample period for the data feed"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, filename="sma_crossover.log")

    run_strategy(args.data_path, args.resample_period)
