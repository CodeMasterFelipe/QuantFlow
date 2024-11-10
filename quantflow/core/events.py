from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process(self, handler):
        pass

    def get_type(self):
        return self.__class__.__name__


class MarketEvent(Event):
    def process(self, handler):
        return handler.process_market_event(self)


class SignalEvent(Event):
    def process(self, handler):
        return handler.process_signal_event(self)


class FillEvent(Event):
    def process(self, handler):
        return handler.process_fill_event(self)


class OrderRequestEvent(Event):
    def process(self, handler):
        return handler.process_order_request_event(self)
