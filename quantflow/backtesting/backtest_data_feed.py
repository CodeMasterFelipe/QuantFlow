from quantflow.core.data_feed import DataFeed
from typing import Generator
import pandas as pd


class BacktestDataFeed(DataFeed):
    def __init__(self, historical_data, datetime_col: str | None = None):
        self.historical_data = pd.read_csv(historical_data)
        if datetime_col:
            self.historical_data[datetime_col] = pd.to_datetime(
                self.historical_data[datetime_col]
            )
            self.historical_data.set_index(datetime_col, inplace=True)

    def resample(self, period: str):
        self.historical_data = (
            self.historical_data.resample(period)
            .agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            .dropna()
        )

    def __iter__(self) -> Generator:
        for _, row in self.historical_data.iterrows():
            yield row.to_dict()
