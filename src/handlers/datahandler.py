""" This module is responsible for handling the data. """
from abc import ABC, abstractmethod
from datetime import datetime

import mysql.connector
import pandas as pd

# Type aliases
Entry = tuple[str, float, float, float, float, float, int]

class DataHandler(ABC):
    @abstractmethod
    def get_latest_bar(self, symbol: str) -> Entry: # type: ignore
        pass

    @abstractmethod
    def get_latest_bars(self, symbol: str, number_of_bars: int):
        pass

    @abstractmethod
    def get_latest_bar_datetime(self, symbol: str) -> datetime:
        pass

    @abstractmethod
    def get_latest_bar_value(self, symbol: str, val_type: str) -> float:
        pass

    @abstractmethod
    def get_latest_bar_values(self, symbol: str, val_type: str, number_of_vals: int) -> list:
        pass

    @abstractmethod
    def update(self):
        pass

class MySQLDataHandler(DataHandler):
    def __init__(self, host: str, user: str, password: str, database: str, tables: dict, start_date:datetime=datetime(2000, 1, 1)):
        # Initialize variables
        self.total_data = {}
        self.date = start_date
        empty = {
            'datetime':[],
            'open':[],
            'high':[],
            'low':[],
            'close':[],
            'adj_close':[],
            'volume':[]
        }

        self.data = {symbol:empty.copy() for symbol in tables}

        # Connect to database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create cursor
        cursor = conn.cursor()

        for symbol in tables:
            table = tables[symbol]
            query = f"""SELECT entry_time, open_price, high_price, low_price, close_price, adj_price, volume
                       FROM {table}
                       WHERE entry_time >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}'
                       ORDER BY entry_time ASC"""
            
            
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall())
            self.total_data[symbol] = df[df[0] >= start_date]
        
        cursor.close()
        conn.close()

        self.counter = -1
        self.continue_backtest = True # Set to false when out of data, or counter > number of trading periods

    def __validate_symbol(self, symbol: str):
        if symbol not in self.data:
            raise ValueError(f"Symbol {symbol} not available in data handler.")
    
    def get_latest_bar(self, symbol: str) -> Entry:
        self.__validate_symbol(symbol)
        
        # Check if data is available or empty
        if not self.data[symbol]['datetime']:
            return None
        
        return (self.data[symbol]['datetime'][-1],
                self.data[symbol]['open'][-1],
                self.data[symbol]['high'][-1],
                self.data[symbol]['low'][-1],
                self.data[symbol]['close'][-1],
                self.data[symbol]['adj_close'][-1],
                self.data[symbol]['volume'][-1])
    
    def get_latest_bars(self, symbol: str, number_of_bars: int = 1) -> list[Entry]:
        self.__validate_symbol(symbol)

        bars = []
        number_of_bars = min(number_of_bars, len(self.data[symbol]['datetime']))

        for i in range(len(self.data[symbol]['datetime']) - number_of_bars, len(self.data[symbol]['datetime'])):
            bars.append((self.data[symbol]['datetime'][i], 
                         self.data[symbol]['open'][i], 
                         self.data[symbol]['high'][i], 
                         self.data[symbol]['low'][i], 
                         self.data[symbol]['close'][i], 
                         self.data[symbol]['adj_close'][i], 
                         self.data[symbol]['volume'][i]))

        return bars
    
    def get_latest_bar_datetime(self, symbol: str) -> datetime:
        self.__validate_symbol(symbol)
        return self.data[symbol]['datetime'][-1]
    
    def get_latest_bar_value(self, symbol: str, val_type: str) -> float:
        self.__validate_symbol(symbol)
        return self.data[symbol][val_type][-1]
    
    def get_latest_bar_values(self, symbol: str, val_type: str, number_of_vals: int = 1) -> list:
        self.__validate_symbol(symbol)
        
        vals = []
        number_of_vals = min(number_of_vals, len(self.data[symbol][val_type]))

        for i in range(len(self.data[symbol][val_type]) - number_of_vals, len(self.data[symbol][val_type])):
            vals.append(self.data[symbol][val_type][i])

        return vals
    
    def update(self):
        if not self.continue_backtest:
            return

        self.counter += 1

        for symbol, dataframe in self.total_data.items():
            if self.counter < len(self.total_data[symbol]):
                self.data[symbol]['datetime'].append(dataframe.iloc[self.counter, 0])
                self.data[symbol]['open'].append(dataframe.iloc[self.counter, 1])
                self.data[symbol]['high'].append(dataframe.iloc[self.counter, 2])
                self.data[symbol]['low'].append(dataframe.iloc[self.counter, 3])
                self.data[symbol]['close'].append(dataframe.iloc[self.counter, 4])
                self.data[symbol]['adj_close'].append(dataframe.iloc[self.counter, 5])
                self.data[symbol]['volume'].append(dataframe.iloc[self.counter, 6])
            else:
                self.continue_backtest = False
                return
                