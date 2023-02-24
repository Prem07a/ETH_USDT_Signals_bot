from binance.client import Client
import requests
import time
from datetime import datetime
from math import ceil


class TradingBot:
    """
    A class that represents a trading bot.

    Attributes:
    - starting_balance (float): the starting balance of the trading account
    - trade (int): the number of trades executed by the bot
    - my_keyb (str): the Binance API key
    - my_secret (str): the Binance secret key
    - my_key (str): the TAAPI.IO API key
    - macd (float): the Moving Average Convergence Divergence (MACD) value
    - histogram (float): the histogram value of the MACD
    - signal (float): the signal line value of the MACD
    - vwap (float): the Volume Weighted Average Price (VWAP)
    - latest_close (float): the latest closing price of the trading pair
    - profit (float): the total profit made by the bot
    - Start (bool): a flag indicating if the bot is starting up
    - buy_price (float): the price at which the bot bought the trading pair
    - sell_price (float): the price at which the bot sold the trading pair
    """

    def __init__(self, binance_api_key, binance_secret_key, taapi_io_api_key, daily_trade=5):
        """
        Initializes a TradingBot object with the specified API keys and daily trade limit.

        Args:
        - binance_api_key (str): the Binance API key
        - binance_secret_key (str): the Binance secret key
        - taapi_io_api_key (str): the TAAPI.IO API key
        - daily_trade (int): the maximum number of trades the bot can execute per day (default is 5)
        """
        self.starting_balance = 20000
        self.trade = 0
        self.my_keyb = binance_api_key
        self.my_secret = binance_secret_key
        self.my_key = taapi_io_api_key
        self.macd = self.histogram = self.signal = self.vwap = self.latest_close = 0
        self.profit = 0
        self.Start = True
        self.buy_price = self.sell_price = 0
        self.wait()
        self.start()

    def wait(self):
        """
        Pauses the bot until the current time is a multiple of 5 minutes (e.g., 10:00, 10:05, 10:10, etc.).
        """
        while True:
            # Get the current minute and second
            minute = int((str(datetime.now()).split()[1].split(":")[1]))
            second = float(str(datetime.now()).split()[1].split(":")[2])

            # Check if the current time is a multiple of 5 minutes
            if minute % 5 == 0 and second < 10:
                # Print a message if the bot is starting up
                if self.Start:
                    self.Start = False
                    print('Starting the trade....')
                return
            else:
                # Wait for the next minute to start
                time.sleep(60 - round(float(second)))

    def get_price_data(self):
        """
        Gets the latest 5-minute candle data for the ETH/USDT trading pair from Binance API.
        """
        # Initialize the Binance API client
        self.client = Client(api_key=self.my_keyb, api_secret=self.my_secret)

        # Get the latest 5-minute candle data for the ETH/USDT trading pair
        self.candles = self.client.get_klines(
            symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)

        # Get the latest closing price from the candle data
        self.latest_close = float(self.candles[-1][4])

    def get_indicator_values(self):
        """
        Calls the TAAPI API to get the MACD and VWAP indicator values for the ETH/USDT trading pair.
        """
        # Define the API endpoint URL
        endpoint = "https://api.taapi.io/bulk"

        # Define a JSON body with parameters to be sent to the API
        parameters = {
            "secret": self.my_key,
            "construct": {
                "exchange": "binance",
                "symbol": "ETH/USDT",
                "interval": "5m",
                "indicators": [
                    {
                        "indicator": "macd"
                    },
                    {
                        "indicator": "vwap",
                        'anchorPeriod': "session"
                    }
                ]
            }
        }

        # Send a POST request to the API with the parameters and get the response
        response = requests.post(url=endpoint, json=parameters)
        info = response.json()

        # Extract the MACD and VWAP values from the response and store them in instance variables
        try:
            self.macd = info['data'][0]["result"]['valueMACD']
            self.signal = info['data'][0]["result"]['valueMACDSignal']
            self.histogram = info['data'][0]["result"]['valueMACDHist']

            # Get the VWAP value and convert it to a float
            self.vwap = float(info['data'][1]["result"]['value'])
        except:
            # Print an error message if there was an issue getting the indicator values
            print('Error HRS')
            self.trade -= 1

    def buying_condition(self):
        """
        Checks if the buying conditions are met, and opens a long position if they are.
        """
        print('Checking Buying Condition...')
        if self.histogram > 0 and self.macd > self.signal and self.vwap < self.latest_close:
            self.buy_price = self.latest_close
            print(f'Long Position Taken at {self.buy_price}')
            self.wait_for_selling()
            print(f'Position Closed at {self.sell_price}')
            self.trade += 1

    def selling_condition(self):
        """
        Checks if the selling conditions are met, and closes the long position if they are.
        """
        print('Checking Selling Condition...')
        if self.histogram < 0 and self.macd < self.signal and self.vwap > self.latest_close:
            self.sell_price = self.latest_close
            print(f'Short sell at {self.sell_price}')
            self.wait_for_buying()
            print(f'Position Squared off at {self.buy_price}')
            self.trade += 1

    def wait_for_buying(self):
        """
        Waits until the conditions are met for opening a long position or the sell price is greater than or equal to 1% of the latest close price.
        """
        while True:
            time.sleep(10)
            self.wait()
            self.get_indicator_values()
            self.get_price_data()
            if (self.histogram > 0 and self.macd > self.signal and self.vwap < self.latest_close) or (self.sell_price*1.01 <= self.latest_close) or (self.sell_price*1.01 >= self.latest_close):
                self.buy_price = self.latest_close
                self.update_wallet()
                return

    def wait_for_selling(self):
        """
        Waits until the conditions are met for closing the long position or the buy price is less than or equal to 1% of the latest close price.
        """
        while True:
            time.sleep(10)
            self.wait()
            self.get_indicator_values()
            self.get_price_data()
            if (self.histogram < 0 and self.macd < self.signal and self.vwap > self.latest_close) or (self.buy_price*0.99 >= self.latest_close) or (self.buy_price*0.99 <= self.latest_close):
                self.sell_price = self.latest_close
                self.update_wallet()
                return

    def update_wallet(self):
        """
        Updates the Wallet Price as per the profit gained.
        """
        self.starting_balance += ((self.sell_price - self.buy_price)
                                  * 5*self.starting_balance/self.sell_price)

    def start(self):
        """
        Starts the Trading Bot and runs the buying and selling conditions repeatedly until Daily Trade Limit is reached.
        """
        while True or (Daily_trade == self.trade):
            print()

            # Get latest price data and indicator values
            self.get_price_data()
            self.get_indicator_values()

            # Check for buying and selling conditions
            self.buying_condition()
            self.selling_condition()

            # Print trade information
            print(
                f'Total Trades: {self.trade} | Profit: {(self.starting_balance-20000)/200}% | Current Balance: {self.starting_balance}')

            # Wait for 10 seconds before checking conditions again
            time.sleep(10)

            # Wait until the next 5-minute mark before checking conditions again
            self.wait()
