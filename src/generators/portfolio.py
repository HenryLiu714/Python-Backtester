from generators.event_queue import EventQueue
from handlers.datahandler import DataHandler
from events.events import FillEvent, SignalEvent

class Portfolio(object):
    """A portfolio object represents all of the user's current holdings
    and cash balance. It is also responsible for generating new orders
    and updating the portfolio based on new events.

    Attributes:
        data_handler (DataHandler): The DataHandler object providing data to the portfolio.
        event_queue (EventQueue): The EventQueue object providing events to the portfolio.
        balance (float): The user's current cash balance.
        positions (dict): A dictionary containing the user's current holdings.
        total_value (float): The total value of the user's portfolio, including balance and holdings.
    """
    def __init__(self, data_handler: DataHandler, event_queue: EventQueue, balance: float):
        """Constructor method

        Args:
            data_handler (DataHandler): The data handler object providing data to the portfolio.
            event_queue (EventQueue): The event queue object providing events to the portfolio.
            balance (float): The user's starting cash balance.
        """

        # Handlers
        self.data_handler = data_handler
        self.event_queue = event_queue

        # Stock holdings
        self.positions = {}
        
        # Equity
        self.balance = balance
        self.total_value = balance

    def update(self):
        """Updates the user's balance and total value based on the current price of assets. Called
        upon a new MarketEvent.
        """
        pass

    def update_fill(self, fill_event: FillEvent):
        """Updates the portfolio based on a new FillEvent.

        Args:
            fill_event (Event): The FillEvent being used to update the portfolio.
        """

        # Validate event type
        if fill_event.type != 'FILL':
            return

    def update_signal(self, signal_event: SignalEvent):
        """Generates a new order based on a new SignalEvent. Either adds a new OrderEvent or None,
        if no order is to be made.

        Args:
            signal_event (Event): The SignalEvent being used to generate a new order.
        """
        # Validate event type
        if signal_event.type != 'SIGNAL':
            return

    def print_status(self):
        """Prints a summary of the user's current portfolio to the console, including positions, balance, and total value.
        """
        print(f'Portfolio Summary: Cash={self.balance}, Total Value={self.total_value},\nPositions:{self.positions}')