import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

# =========================
# GET NIFTY 200 STOCKS
# =========================

wiki_url = "https://en.wikipedia.org/wiki/NIFTY_200"

tables = pd.read_html(wiki_url)

stocks = None

for table in tables:
    cols = [str(c).lower() for c in table.columns]

    if any("symbol" in c for c in cols):
        stocks = table
        break

if stocks is None:
    raise Exception("Could not find Nifty 200 table")

symbol_col = [c for c in stocks.columns if "symbol" in str(c).lower()][0]

symbols = (
    stocks[symbol_col]
    .astype(str)
    .str.strip()
    .str.upper()
    + ".NS"
).tolist()

print(f"Loaded {len(symbols)} stocks")

# =========================
# RESULTS
# =========================

buy_signals = []
watchlist = []

# =========================
# SCAN
# =========================

for symbol in symbols:

    try:

        print(f"Scanning {symbol}")

        # DAILY DATA

        daily = yf.download(
            symbol,
            period="1y",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if len(daily) < 220:
            continue

        close_daily = daily["Close"].iloc[:, 0]

        ema100 = EMAIndicator(
            close_daily,
            window=100
        ).ema_indicator()

        ema200 = EMAIndicator(
            close_daily,
            window=200
        ).ema_indicator()

        daily_rsi = RSIIndicator(
            close_daily,
            window=14
        ).rsi()

        # INTRADAY

        intraday = yf.download(
            symbol,
            period="60d",
            interval="30m",
            auto_adjust=True,
            progress=False
        )

        if len(intraday) < 220:
            continue

        close_30 = intraday["Close"].iloc[:, 0]

        rsi30 = RSIIndicator(
            close_30,
            window=14
        ).rsi()

        macd_obj = MACD(close_30)

        macd = macd_obj.macd()
        signal = macd_obj.macd_signal()

        volume = intraday["Volume"].iloc[:, 0]

        avg_volume = volume.tail(20).mean()

        latest_volume = volume.iloc[-1]

        latest_close = float(close_daily.iloc[-1])

        # CONDITIONS

        trend_ok = (
            latest_close > ema200.iloc[-1]
            and ema100.iloc[-1] > ema200.iloc[-1]
        )

        momentum_ok = (
            rsi30.iloc[-1] > 55
            and macd.iloc[-1] > signal.iloc[-1]
        )

        volume_ok = (
            latest_volume > avg_volume
        )

        # BUY

        if trend_ok and momentum_ok and volume_ok:

            buy_signals.append({
                "Symbol": symbol,
                "Close": round(latest_close, 2),
                "RSI": round(rsi30.iloc[-1], 2),
                "MACD": round(macd.iloc[-1], 2)
            })

        # WATCHLIST

        elif trend_ok:

            watchlist.append({
                "Symbol": symbol,
                "Close": round(latest_close, 2),
                "RSI": round(rsi30.iloc[-1], 2)
            })

    except Exception as e:

        print(symbol, e)

# =========================
# SAVE RESULTS
# =========================

buy_df = pd.DataFrame(buy_signals)
watch_df = pd.DataFrame(watchlist)

buy_df.to_csv(
    "buy_signals.csv",
    index=False
)

watch_df.to_csv(
    "watchlist.csv",
    index=False
)

print()
print("BUY SIGNALS")
print(buy_df)

print()
print("WATCHLIST")
print(watch_df)
