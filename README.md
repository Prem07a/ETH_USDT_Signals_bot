# ETH_USDT_Signals_bot
This bot gives Buying and selling signals for Etherum Trading.<br>

This is a Python program that simulates a trading bot for the ETH/USDT trading pair on the Binance exchange. The bot uses technical analysis indicators to determine whether to buy, sell or hold the trading pair.

## INSTALLATION
1. Clone the repository:

```
git clone https://github.com/Prem07a/ETH_USDT_Signals_bot
```

2. Install the Required packages:
```
pip install -r requirements.txt
```

## USAGE
1. To use the trading bot, open the main.py file and update the following variables with your own API keys:
* BINANCE_API_KEY: Your Binance API key
* BINANCE_SECRET_KEY: Your Binance secret key
* TAAPI_IO_API_KEY: Your TAAPI.IO API key

2. Run the main.py file to start the trading bot.
```
python main.py
```
> The bot will start executing trades every 5 minutes, based on the technical analysis indicators.

3. To stop the bot, press 'CTR + C'.

## Technical Analysis Indicators:
* Moving Average Convergence Divergence (MACD): The MACD indicator shows the relationship between two moving averages of the price of the trading pair. A buy signal is generated when the MACD line crosses above the signal line, indicating that the price is likely to increase.
* Volume Weighted Average Price (VWAP): The VWAP indicator calculates the average price of the trading pair over a given time period, weighted by the trading volume. This gives a more accurate picture of the true price of the trading pair, and can help to identify trends.
* Histogram: The histogram is the difference between the MACD line and the signal line. A positive histogram indicates that the price is increasing, while a negative histogram indicates that the price is decreasing.

## Disclamier
This trading bot is for educational purposes only and should not be used for real trading. The bot is provided "as is" without warranty of any kind, express or implied. The author is not responsible for any losses or damages that may result from the use of this program
