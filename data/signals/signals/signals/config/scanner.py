import pandas as pd

stocks = pd.read_csv("data/nifty200.csv")

symbols = stocks["symbol"].tolist()

print(f"Loaded {len(symbols)} stocks")

for symbol in symbols:
    print(symbol)
