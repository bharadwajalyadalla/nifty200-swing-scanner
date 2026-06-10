import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

symbol = "INFY.NS"

# Daily data
daily = yf.download(
    symbol,
    period="1y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

daily["EMA100"] = EMAIndicator(daily["Close"], window=100).ema_indicator()
daily["EMA200"] = EMAIndicator(daily["Close"], window=200).ema_indicator()
daily["RSI"] = RSIIndicator(daily["Close"], window=14).rsi()

print("DAILY")

print("Close:", round(daily["Close"].iloc[-1], 2))
print("EMA100:", round(daily["EMA100"].iloc[-1], 2))
print("EMA200:", round(daily["EMA200"].iloc[-1], 2))
print("RSI:", round(daily["RSI"].iloc[-1], 2))

# 30 minute data
intraday = yf.download(
    symbol,
    period="60d",
    interval="30m",
    auto_adjust=True,
    progress=False
)

intraday["EMA100"] = EMAIndicator(intraday["Close"], window=100).ema_indicator()
intraday["EMA200"] = EMAIndicator(intraday["Close"], window=200).ema_indicator()

macd = MACD(intraday["Close"])

intraday["MACD"] = macd.macd()
intraday["SIGNAL"] = macd.macd_signal()

intraday["RSI"] = RSIIndicator(
    intraday["Close"],
    window=14
).rsi()

print("\n30 MIN")

print("Close:", round(intraday["Close"].iloc[-1], 2))
print("EMA100:", round(intraday["EMA100"].iloc[-1], 2))
print("EMA200:", round(intraday["EMA200"].iloc[-1], 2))
print("RSI:", round(intraday["RSI"].iloc[-1], 2))
print("MACD:", round(intraday["MACD"].iloc[-1], 2))
print("Signal:", round(intraday["SIGNAL"].iloc[-1], 2))
