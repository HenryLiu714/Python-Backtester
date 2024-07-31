from events.events import OrderEvent, SignalEvent

class OrderGenerator(object):
    def __init__(self):
        pass
    def generate_order(self, signal: SignalEvent):
        return None
    
class NaiveOrderGenerator(OrderGenerator):
    def generate_order(self, signal: SignalEvent):
        if signal.direction == 'LONG':
            return OrderEvent(symbol=signal.symbol, timestamp=signal.timestamp, order_type='market', quantity=1)
        else:
            return OrderEvent(symbol=signal.symbol, timestamp=signal.timestamp, order_type='market', quantity=-1)