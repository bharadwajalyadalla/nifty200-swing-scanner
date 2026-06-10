import pandas as pd
import yfinance as yf

stocks = pd.read_csv("data/nifty200.csv")

symbols = stocks["symbol"].tolist()

print(f"Loaded {len(symbols)} stocks")

for symbol in symbols:
    try:
        df = yf.download(
            symbol,
            period="5d",
            interval="30m",
            auto_adjust=True,
            progress=False
        )

        if not df.empty:
            close = float(df["Close"].iloc[-1])
            print(f"{symbol}: {close}")

    except Exception as e:
        print(f"{symbol}: Error {e}")
