from generators.portfolio import Portfolio
from generators.strategy import Strategy
from generators.event_queue import EventQueue
from handlers.datahandler import DataHandler
from handlers.executionhandler import ExecutionHandler

class BackTest(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    def __init__(self,
                 symbols_list: list[str],
                 strategy: Strategy,
                 data_handler: DataHandler,
                 initial_capital: float = 100000.0,
                 commission: float = 0,
                 fill_cost: float = 0.87,
                 start_date: str = '2000-01-01',
                 max_trading_periods: int = float('inf'),
                 portfolio: Portfolio = None,
                 execution_handler: ExecutionHandler = None
                 ):
        """Constructor method
        """
        self.symbols_list = symbols_list
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.fill_cost = fill_cost
        self.start_date = start_date
        self.max_trading_periods = max_trading_periods
        self.data_handler = data_handler

        self.event_queue = EventQueue()
        
        self.portfolio = Portfolio(self.data_handler, self.event_queue, initial_capital)
        self.execution_handler = ExecutionHandler(self.event_queue, commission, fill_cost)

        if portfolio:
            self.portfolio = portfolio 

        if execution_handler:
            self.execution_handler = execution_handler
        
    def run_backtest():
        pass

    def print_results():
        pass