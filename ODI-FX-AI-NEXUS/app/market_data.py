"""
ODI FX AI NEXUS

Market Data Engine V1
"""

import random
from datetime import datetime


def generate_candles(count=500):
    """
    Generates simulated XAUUSD candles.

    This will later be replaced with
    live market data.
    """

    candles = []

    price = 3350.00

    for _ in range(count):

        open_price = price

        high_price = open_price + random.uniform(0.20, 5.00)

        low_price = open_price - random.uniform(0.20, 5.00)

        close_price = random.uniform(
            low_price,
            high_price
        )

        volume = random.randint(
            500,
            5000
        )

        candles.append({

            "open": round(open_price, 2),

            "high": round(high_price, 2),

            "low": round(low_price, 2),

            "close": round(close_price, 2),

            "volume": volume

        })

        price = close_price

    return candles


def get_market_data():
    """
    Returns the current market snapshot.
    """

    candles = generate_candles()

    current = candles[-1]

    return {

        "symbol": "XAUUSD",

        "price": current["close"],

        "bid": round(current["close"] - 0.10, 2),

        "ask": round(current["close"] + 0.10, 2),

        "spread": 0.20,

        "volume": current["volume"],

        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),

        "candles": candles

    }