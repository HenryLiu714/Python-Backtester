from collections import deque
from events.events import Event

class EventQueue:
    def __init__(self):
        self.queue = deque()

    def get_next(self):
        return self.queue.popleft()
    
    def put(self, event: Event):
        self.queue.append(event)
    
    def is_empty(self):
        return len(self.queue) == 0