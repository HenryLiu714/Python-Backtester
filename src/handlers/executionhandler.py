from generators.event_queue import EventQueue
from events.events import Event, OrderEvent, FillEvent

class ExecutionHandler(object):
    def __init__(self, event_queue: EventQueue, commission: float, fill_cost: float):
        self.commission = commission
        self.fill_cost = fill_cost

        self.event_queue = event_queue

    def execute_order(self, order_event: Event):
        if order_event.type != 'ORDER':
            return

        fill_event = FillEvent(
            order_event.symbol,
            order_event.quantity,
            order_event.direction,
            order_event.entry_time,
            self.fill_cost,
            self.commission
        )

        self.event_queue.put(fill_event)