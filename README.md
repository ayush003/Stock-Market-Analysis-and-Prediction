# Algorithmic Stock Markets Prediction Bot

## Runnning the code

`cd bot_scripts; python3 test.py <csvfile>` where <csvfile> is the OHLC data file for any given stock. The bot predicts the movement of stock price in future based on the OHLC(Open-High-Low-Close) prices in the past.

## Directory structure

1. `algo` contains scripts used for analysis and testing of the individual techinical indicators (Moving Averages, Bollinger Bands, Support and Resistance, Candlestick Patterns)
2. `bot_scripts` contains all the scripts required for running the bot and testing the accuracy of prediction.
3. `data` contains OHLC price data for various tickers collected from the official BSE website, in csv format.


