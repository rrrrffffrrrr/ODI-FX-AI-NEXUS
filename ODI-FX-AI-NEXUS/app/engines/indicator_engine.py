"""
ODI FX AI NEXUS

Indicator Engine V1
"""

from statistics import mean


class IndicatorEngine:

    def __init__(self):
        pass

    def ema(self, prices, period):

        if len(prices) < period:

            return None

        multiplier = 2 / (period + 1)

        ema = mean(prices[:period])

        for price in prices[period:]:

            ema = (price - ema) * multiplier + ema

        return round(ema, 2)

    def rsi(self, prices, period=14):

        if len(prices) <= period:

            return 50

        gains = []
        losses = []

        for i in range(1, period + 1):

            change = prices[-i] - prices[-i - 1]

            if change >= 0:

                gains.append(change)
                losses.append(0)

            else:

                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:

            return 100

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)

    def analyse(self, market):

        candles = market["candles"]

        closes = [c["close"] for c in candles]

        ema20 = self.ema(closes, 20)
        ema50 = self.ema(closes, 50)
        ema100 = self.ema(closes, 100)
        ema200 = self.ema(closes, 200)

        rsi = self.rsi(closes)

        volume = candles[-1]["volume"]

        avg_volume = sum(
            c["volume"] for c in candles[-20:]
        ) / 20

        if volume > avg_volume:

            volume_state = "High"

        else:

            volume_state = "Low"

        if ema20 > ema50:

            ema_bias = "Bullish"

        elif ema20 < ema50:

            ema_bias = "Bearish"

        else:

            ema_bias = "Neutral"

        if ema20 > ema50 > ema100 > ema200:

            trend_strength = "Strong Bullish"

        elif ema20 < ema50 < ema100 < ema200:

            trend_strength = "Strong Bearish"

        else:

            trend_strength = "Mixed"

        if rsi >= 70:

            momentum = "Overbought"

        elif rsi <= 30:

            momentum = "Oversold"

        else:

            momentum = "Healthy"

        return {

            "ema20": ema20,

            "ema50": ema50,

            "ema100": ema100,

            "ema200": ema200,

            "ema": ema_bias,

            "trend_strength": trend_strength,

            "rsi": rsi,

            "momentum": momentum,

            "macd": "Coming Soon",

            "volume": volume_state

        }