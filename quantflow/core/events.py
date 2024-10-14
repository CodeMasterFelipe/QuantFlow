from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process(self, handler):
        pass

    def get_type(self):
        return self.__class__.__name__

