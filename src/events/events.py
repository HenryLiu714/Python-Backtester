"""File containing the Event classes for the trading system."""

from abc import ABC

class Event(ABC):
    """_summary_

    :param _type_ ABC: _description_
    """
    pass

class MarketEvent(Event):
    """_summary_

    :param _type_ Event: _description_
    """
    def __init__(self):
        """_summary_
        """
        self.type = 'MARKET'

class SignalEvent(Event):
    """_summary_

    :param _type_ Event: _description_
    """
    def __init__(self, symbol: str, timestamp: str, direction: bool, strength: float):
        """_summary_

        :param str symbol: _description_
        :param str timestamp: _description_
        :param bool direction: _description_
        :param float strength: _description_
        """
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.timestamp = timestamp
        self.direction = direction
        self.strength = strength
    
class OrderEvent(Event):
    """_summary_

    :param _type_ Event: _description_
    """
    def __init__(self, symbol: str, timestamp: str, order_type: str = 'market', quantity: int = 1):
        """_summary_

        :param str symbol: _description_
        :param str timestamp: _description_
        :param str order_type: _description_, defaults to 'market'
        :param int quantity: _description_, defaults to 1
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.timestamp = timestamp
        self.order_type = order_type
        self.quantity = quantity
    
    def print_order(self):
        """_summary_
        """
        print(f"Order: Symbol={self.symbol}, Timestamp={self.timestamp}, Type={self.order_type}, Quantity={self.quantity}")

class FillEvent(Event):
    """_summary_

    :param _type_ Event: _description_
    """
    def __init__(self, symbol: str, timestamp: str, quantity: int, direction: str, fill_cost: float = 0, commission: float = 0):
        """Constructor method
        """
        self.type = 'FILL'
        self.symbol = symbol
        self.timestamp = timestamp
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission