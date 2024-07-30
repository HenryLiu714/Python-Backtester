from events.events import SignalEvent
from generators.event_queue import EventQueue
from handlers.datahandler import DataHandler

class Strategy(object):
    """An base class for strategy objects, which are responsible for generating trading signals based on market data.

    Attributes:
        data_handler (DataHandler): The DataHandler object providing data to the strategy.
    """
    def __init__(self, data_handler: DataHandler, event_queue: EventQueue):
        self.data_handler = data_handler
        self.event_queue = event_queue

    def calculate_signals(self) -> SignalEvent:
        """Generates a new trading signal based on the current market data.

        Returns:
            SignalEvent: Returns a SignalEvent object containing the symbol and direction of the trade. None if no signal generated.
        """
        return None

    def update(self):
        """Updates the strategy based on new market data. Called upon a new MarketEvent.
        """
        self.event_queue.put(self.calculate_signals())

class SampleStrategy(Strategy):
    pass
