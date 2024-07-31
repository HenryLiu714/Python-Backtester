from generators.event_queue import EventQueue
from handlers.datahandler import DataHandler
from events.events import FillEvent, SignalEvent
from generators.order_generator import OrderGenerator

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
        futures (float): The value of a one point move in the futures contract, default 1 (as 1 point move = $1 for equities).
    """
    def __init__(self, data_handler: DataHandler, event_queue: EventQueue, order_generator: OrderGenerator, balance: float, contract_value: float = 1):
        """Constructor method

        Args:
            data_handler (DataHandler): The data handler object providing data to the portfolio.
            event_queue (EventQueue): The event queue object providing events to the portfolio.
            balance (float): The user's starting cash balance.
        """

        # Handlers
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.order_generator = order_generator

        # Stock holdings
        # Each entry will be a dictionary containing the **starting** price (price when trade was entered) and quantity
        # Example: {"MNQ": {"price": 100, "quantity": 10}}
        self.positions = {}
        
        # Equity
        self.balance = balance
        self.total_value = balance
        self.contract_value = contract_value

    def update(self):
        """Updates the user's balance and total value based on the current price of assets. Called
        upon a new MarketEvent.
        """
        for symbol, position in self.positions.items():
            self.total_value = self.balance

            # Get latest price
            latest_price = self.data_handler.get_latest_bar_value(symbol, 'close')
            change_in_total = (latest_price - position['price']) * position['quantity'] * self.contract_value
            starting_total = position['price'] * position['quantity'] * self.contract_value

            total = starting_total + change_in_total
            self.total_value += total

    def __update_buy(self, position: dict, fill_event: FillEvent):
        """Updates the portfolio based on a new buy FillEvent.

        Args:
            position (dict): The position being updated.
            fill_event (FillEvent): The FillEvent being used to update the portfolio.
        """
        latest_price = self.data_handler.get_latest_bar_value(fill_event.symbol, 'close')
        # Update position
        if position['quantity'] > 0:
            position['price'] = (position['price'] * position['quantity'] + latest_price * fill_event.quantity)/(position['quantity'] + fill_event.quantity)
            position['quantity'] += fill_event.quantity
        else: # Current position is short
            position['quantity'] += fill_event.quantity

            if position['quantity'] > 0:
                position['price'] = latest_price

    def __update_sell(self, position: dict, fill_event: FillEvent):
        """Updates the portfolio based on a new sell FillEvent.

        Args:
            position (dict): The position being updated.
            fill_event (FillEvent): The FillEvent being used to update the portfolio.
        """
        latest_price = self.data_handler.get_latest_bar_value(fill_event.symbol, 'close')
        # Update position
        if position['quantity'] < 0:
            position['price'] = (position['price'] * -position['quantity'] + latest_price * fill_event.quantity)/(-position['quantity'] + fill_event.quantity)
            position['quantity'] -= fill_event.quantity
        else:
            position['quantity'] -= fill_event.quantity

            if position['quantity'] < 0:
                position['price'] = latest_price

    def update_fill(self, fill_event: FillEvent):
        """Updates the portfolio based on a new FillEvent.

        Args:
            fill_event (Event): The FillEvent being used to update the portfolio.
        """

        # Validate event type
        if fill_event.type != 'FILL':
            return
        
        latest_price = self.data_handler.get_latest_bar_value(fill_event.symbol, 'close')
        
        # Update positions
        if fill_event.direction == 'BUY':
            self.balance -= latest_price * fill_event.quantity
            if fill_event.symbol not in self.positions:
                self.positions[fill_event.symbol] = {"price": fill_event.fill_cost, "quantity": fill_event.quantity}
            else:
                self.__update_buy(self.positions[fill_event.symbol], fill_event)
        else:
            self.balance += latest_price * fill_event.quantity
            if fill_event.symbol not in self.positions:
                self.positions[fill_event.symbol] = {"price": fill_event.fill_cost, "quantity": -fill_event.quantity}
            else:
                self.__update_sell(self.positions[fill_event.symbol], fill_event)

        # Update balance
        transaction_value = latest_price * fill_event.quantity
        transaction_fees = transaction_value * fill_event.commission + fill_event.fill_cost * fill_event.quantity
        self.balance -= transaction_fees

    def update_signal(self, signal_event: SignalEvent):
        """Generates a new order based on a new SignalEvent. Either adds a new OrderEvent or None,
        if no order is to be made.

        Args:
            signal_event (Event): The SignalEvent being used to generate a new order.
        """
        # Validate event type
        if signal_event.type != 'SIGNAL':
            return
        
        self.event_queue.put(self.order_generator.generate_order(signal_event))


    def print_status(self):
        """Prints a summary of the user's current portfolio to the console, including positions, balance, and total value.
        """
        print(f'Portfolio Summary: Cash={self.balance}, Total Value={self.total_value},\nPositions:{self.positions}')