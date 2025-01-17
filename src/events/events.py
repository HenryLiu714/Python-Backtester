"""File containing the Event classes for the trading system."""

from abc import ABC

class Event(ABC):
    """An abstract class serving as the base class for all other event types.
    """

class MarketEvent(Event):
    """A MarketEvent object acts as a signal that market data has been updated, signalling
    to the rest of the program that new data is available for processing.

    Attributes:
        type: A string representing the type of event. In this case, 'MARKET'.
    """
    def __init__(self):
        """_summary_
        """
        self.type = 'MARKET'

class SignalEvent(Event):
    """A signal event is generated by a strategy object and represents a trading signal created by our strategy.

    Attributes:
        type: A string representing the type of event. In this case, 'SIGNAL'.
        symbol: A string representing the symbol of the asset being traded.
        timestamp: A string representing the timestamp the signal was generated.
        direction: A boolean representing the direction of the signal. True for long, False for short.
        strength: A float representing the strength of the signal. Can be adjusted to user preference.
    """
    def __init__(self, symbol: str, timestamp: str, direction: bool, strength: float = 0):
        """Constructor method

        Args:
            symbol (str): The symbol of the asset being traded.
            timestamp (str): The timestamp the signal was generated.
            direction (bool): The direction of the signal. True for long, False for short.
            strength (float): The strength of the signal (dependant on user preference). Defaults to 0. 
        """        
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.timestamp = timestamp
        self.direction = direction
        self.strength = strength
    
class OrderEvent(Event):
    """An OrderEvent object represents an order to be executed in the market. This is typically generated
    by our Portfolio as a result of a signal.

    Attributes:
        type: A string representing the type of event. In this case, 'ORDER'.
        symbol: A string representing the symbol of the asset being traded.
        timestamp: A string representing the timestamp the order was generated.
        order_type: A string representing the type of order. Can be 'market' or 'limit'.
        quantity: An integer representing the quantity of the asset being traded.
    """
    def __init__(self, symbol: str, timestamp: str, order_type: str = 'market', quantity: int = 1):
        """Constructor method

        Args:
            symbol (str): The symbol of the asset being traded.
            timestamp (str): The timestamp the order was generated.
            order_type (str, optional): The type of order, examples being market or limit. Defaults to 'market'.
            quantity (int, optional): The quantity of the asset being traded. Defaults to 1.
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.timestamp = timestamp
        self.order_type = order_type
        self.quantity = quantity
    
    def print_order(self):
        """Prints a summary of the order event to the console.
        """
        print(f"Order: Symbol={self.symbol}, Timestamp={self.timestamp}, Type={self.order_type}, Quantity={self.quantity}")

class FillEvent(Event):
    """A FillEvent object represents a filled order in the market. This event is generated by the ExecutionHandler
    from an order.

    Attributes:
        type: A string representing the type of event. In this case, 'FILL'.
        symbol: A string representing the symbol of the asset being traded.
        timestamp: A string representing the timestamp the order was filled.
        quantity: An integer representing the quantity of the asset being traded.
        direction: A string representing the direction of the fill. Can be 'BUY' or 'SELL'.
        fill_cost: A float representing the cost of the fill. A flat fee added to the total price of the order.
        commission: A float representing the commission cost, a percentage of the total order.
    """
    def __init__(self, symbol: str, timestamp: str, quantity: int, direction: str, fill_cost: float = 0, commission: float = 0):
        """Constructor method

        Args:
            symbol (str): The symbol of the asset being traded.
            timestamp (str): The timestamp the order was filled.
            quantity (int): The quantity of the asset being traded.
            direction (str): The direction of the fill. Can be 'BUY' or 'SELL'.
            fill_cost (float, optional): The cost of the fill, a flat fee added onto the cost of the trade. Defaults to 0.
            commission (float, optional): The commission of the order as a percent of the total order price. Defaults to 0.
        """
        self.type = 'FILL'
        self.symbol = symbol
        self.timestamp = timestamp
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission