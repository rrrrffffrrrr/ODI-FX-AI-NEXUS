"""
ODI FX AI NEXUS

Signal Engine V1
"""


class SignalEngine:

    def __init__(self):
        pass

    def generate(
        self,
        market,
        trend,
        indicators,
        structure,
        support_resistance,
        liquidity,
        order_block,
        fvg,
        mtf
    ):

        score = 0

        reasons = []

        # =====================================
        # TREND
        # =====================================

        if trend["trend"] == "Bullish":

            score += 20

            reasons.append("Bullish trend confirmed.")

        elif trend["trend"] == "Bearish":

            score -= 20

            reasons.append("Bearish trend confirmed.")

        # =====================================
        # EMA
        # =====================================

        if indicators["ema"] == "Bullish":

            score += 15

            reasons.append("EMA alignment bullish.")

        elif indicators["ema"] == "Bearish":

            score -= 15

            reasons.append("EMA alignment bearish.")

        # =====================================
        # MARKET STRUCTURE
        # =====================================

        if structure["structure"] == "Bullish":

            score += 15

            reasons.append("Bullish market structure.")

        elif structure["structure"] == "Bearish":

            score -= 15

            reasons.append("Bearish market structure.")

        # =====================================
        # LIQUIDITY
        # =====================================

        if liquidity["buy_side"]:

            score += 10

            reasons.append("Buy-side liquidity identified.")

        if liquidity["sell_side"]:

            score -= 10

            reasons.append("Sell-side liquidity identified.")

        # =====================================
        # ORDER BLOCK
        # =====================================

        if order_block["type"] == "Bullish":

            score += 10

            reasons.append("Bullish Order Block.")

        elif order_block["type"] == "Bearish":

            score -= 10

            reasons.append("Bearish Order Block.")

        # =====================================
        # FAIR VALUE GAP
        # =====================================

        if fvg["direction"] == "Bullish":

            score += 10

            reasons.append("Bullish Fair Value Gap.")

        elif fvg["direction"] == "Bearish":

            score -= 10

            reasons.append("Bearish Fair Value Gap.")

        # =====================================
        # MULTI-TIMEFRAME
        # =====================================

        if mtf["alignment"]:

            score += 20

            reasons.append("Timeframes aligned.")

        # =====================================
        # FINAL DECISION
        # =====================================

        if score >= 70:

            signal = "BUY"

            grade = "A+"

        elif score <= -70:

            signal = "SELL"

            grade = "A+"

        else:

            signal = "WAIT"

            grade = "C"

        current = market["price"]

        entry_low = round(current - 0.30, 2)

        entry_high = round(current + 0.30, 2)

        if signal == "BUY":

            sl = round(current - 6.00, 2)

            tp1 = round(current + 8.00, 2)

            tp2 = round(current + 16.00, 2)

            tp3 = round(current + 24.00, 2)

        elif signal == "SELL":

            sl = round(current + 6.00, 2)

            tp1 = round(current - 8.00, 2)

            tp2 = round(current - 16.00, 2)

            tp3 = round(current - 24.00, 2)

        else:

            sl = "-"

            tp1 = "-"

            tp2 = "-"

            tp3 = "-"

        confidence = min(max(abs(score), 0), 100)

        return {

            "signal": signal,

            "grade": grade,

            "confidence": confidence,

            "entry_low": entry_low,

            "entry_high": entry_high,

            "sl": sl,

            "tp1": tp1,

            "tp2": tp2,

            "tp3": tp3,

            "rr": "1 : 3",

            "score": score,

            "reasons": reasons

        }