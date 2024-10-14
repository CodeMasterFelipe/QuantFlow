from quantflow.core.data_feed import DataFeed
from typing import Generator


class BacktestDataFeed(DataFeed):
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def __iter__(self) -> Generator:
        for data in self.historical_data:
            yield data
