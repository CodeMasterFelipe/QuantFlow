from collections import deque


class EventQueue:
    def __init__(self):
        self.events = deque()

    def put(self, event):
        """
        Add a new event to the end of the queue.
        """
        self.events.append(event)

    def get(self):
        """
        Get the next event from the front of the queue.
        If the quesue is empty, return None.
        """
        return self.events.popleft()

    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return len(self.events) == 0
