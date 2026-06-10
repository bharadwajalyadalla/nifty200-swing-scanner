import yfinance as yf
import pandas as pd

symbol = "INFY.NS"

print(f"Downloading data for {symbol}...")

daily = yf.download(
    symbol,
    period="1y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

print("\n===== DATAFRAME INFO =====")
print("Type of daily:", type(daily))

print("\n===== COLUMNS =====")
print(daily.columns)

print("\n===== CLOSE COLUMN TYPE =====")
print(type(daily["Close"]))

print("\n===== CLOSE COLUMN SHAPE =====")
print(daily["Close"].shape)

print("\n===== FIRST 5 ROWS =====")
print(daily.head())

print("\n===== LAST 5 ROWS =====")
print(daily.tail())

print("\n===== LAST CLOSE =====")

try:
    close = daily["Close"].squeeze().iloc[-1]
    print(close)
except Exception as e:
    print("ERROR:", e)
