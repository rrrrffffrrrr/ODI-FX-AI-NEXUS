"""
ODI FX AI NEXUS

Trend Engine V1
"""

class TrendEngine:

    def __init__(self):
        pass

    def analyse(self, market, indicators):

        price = market["price"]

        ema20 = indicators["ema20"]
        ema50 = indicators["ema50"]
        ema100 = indicators["ema100"]
        ema200 = indicators["ema200"]

        rsi = indicators["rsi"]

        score = 0
        reasons = []

        # ==========================
        # EMA ALIGNMENT
        # ==========================

        if ema20 > ema50:

            score += 20
            reasons.append("EMA20 above EMA50")

        if ema50 > ema100:

            score += 20
            reasons.append("EMA50 above EMA100")

        if ema100 > ema200:

            score += 20
            reasons.append("EMA100 above EMA200")

        # ==========================
        # PRICE POSITION
        # ==========================

        if price > ema20:

            score += 10
            reasons.append("Price above EMA20")

        if price > ema50:

            score += 10
            reasons.append("Price above EMA50")

        # ==========================
        # RSI
        # ==========================

        if 50 <= rsi <= 70:

            score += 20
            reasons.append("Healthy bullish RSI")

        elif 30 <= rsi < 50:

            score -= 10
            reasons.append("Weak bearish RSI")

        elif rsi > 70:

            reasons.append("Market becoming overbought")

        elif rsi < 30:

            reasons.append("Market oversold")

        # ==========================
        # DECISION
        # ==========================

        if score >= 80:

            trend = "Bullish"

        elif score <= 30:

            trend = "Bearish"

        else:

            trend = "Sideways"

        return {

            "trend": trend,

            "score": score,

            "reason": f"{trend} trend detected.",

            "reasons": reasons

        }