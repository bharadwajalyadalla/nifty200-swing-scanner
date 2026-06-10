import yfinance as yf

symbol = "INFY.NS"

df = yf.download(
    symbol,
    period="1mo",
    interval="1d",
    auto_adjust=False,
    progress=False
)

print(df.tail())
