from quantflow.core.data_feed import DataFeed
from quantflow.core.event_handler import EventHandler
from quantflow.core.event_queue import EventQueue
from quantflow.core.events import MarketEvent


class TradingEngine:
    def __init__(
        self, data_feed: DataFeed, event_handler: EventHandler, event_queue: EventQueue
    ):
        self.data_feed = data_feed
        self.event_handler = event_handler
        self.event_queue = event_queue

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
