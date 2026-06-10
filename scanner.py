import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

symbol = "INFY.NS"

daily = yf.download(
    symbol,
    period="1y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

close_daily = daily["Close"].iloc[:, 0]

ema100 = EMAIndicator(close_daily, window=100).ema_indicator()
ema200 = EMAIndicator(close_daily, window=200).ema_indicator()
rsi = RSIIndicator(close_daily, window=14).rsi()

print("DAILY")

print("Close:", round(close_daily.iloc[-1], 2))
print("EMA100:", round(ema100.iloc[-1], 2))
print("EMA200:", round(ema200.iloc[-1], 2))
print("RSI:", round(rsi.iloc[-1], 2))

intraday = yf.download(
    symbol,
    period="60d",
    interval="30m",
    auto_adjust=True,
    progress=False
)

close_30m = intraday["Close"].iloc[:, 0]

ema100_30 = EMAIndicator(close_30m, window=100).ema_indicator()
ema200_30 = EMAIndicator(close_30m, window=200).ema_indicator()

macd = MACD(close_30m)

rsi30 = RSIIndicator(close_30m, window=14).rsi()

print("\n30 MIN")

print("Close:", round(close_30m.iloc[-1], 2))
print("EMA100:", round(ema100_30.iloc[-1], 2))
print("EMA200:", round(ema200_30.iloc[-1], 2))
print("RSI:", round(rsi30.iloc[-1], 2))
print("MACD:", round(macd.macd().iloc[-1], 2))
print("Signal:", round(macd.macd_signal().iloc[-1], 2))
