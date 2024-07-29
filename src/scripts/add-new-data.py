from dotenv import load_dotenv
import yfinance as yf
import mysql.connector
import os
import datetime


# This script is used to add new data to the database. Precisely, it adds minutely data
# from the given futures symbol to the MySQL database. The data is fetched from Yahoo Finance.

class AddData(object):
    """AddData class is used to add new financial data to the database.
    """    
    def __init__(self):
        """Constructor function for AddData class.
        """        
        load_dotenv()

    def add_new_data(self, symbol: str, table_name: str) -> None:  
        """Method for gathering and adding new financial data to the database.

        :param str symbol: Symbol of equity or futures to fetch data for.
        :param str table_name: Name of table to insert new data into.
        """        
        futures_db = mysql.connector.connect(
            host = os.environ['DB_HOST'],
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASS'],
            database = os.environ['FUTURES_DB']
            )
        
        start_date = datetime.datetime.today() - datetime.timedelta(days=6)
        end_date = datetime.datetime.today() + datetime.timedelta(days=1)

        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        data = yf.download(symbol, start=start_date, end=end_date, interval='1m')
        data = data.reset_index()

        data['Datetime'] = data['Datetime'].apply(lambda x : x.strftime('%Y-%m-%d %H:%M:%S'))

        add_data = (f"""INSERT IGNORE INTO {table_name}(entry_time, open_price, high_price, low_price, close_price, adj_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)""")

        curs = futures_db.cursor()
        for row in data.itertuples(index=False, name=None):
            curs.execute(add_data, row)

        futures_db.commit()

        curs.close()
        futures_db.close()

data_adder = AddData()
data_adder.add_new_data('MNQ=F', 'mnq')