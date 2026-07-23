"""
ODI FX AI NEXUS

Market Structure Engine V1
"""


class MarketStructureEngine:

    def __init__(self):
        pass

    def analyse(self, market):

        candles = market["candles"]

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        recent_high = max(highs[-20:])
        previous_high = max(highs[-40:-20])

        recent_low = min(lows[-20:])
        previous_low = min(lows[-40:-20])

        structure = "Sideways"
        bos = False
        choch = False
        score = 50
        reasons = []

        # =====================================
        # Bullish Structure
        # =====================================

        if recent_high > previous_high and recent_low > previous_low:

            structure = "Bullish"

            bos = True

            score = 90

            reasons.append("Higher High created")

            reasons.append("Higher Low maintained")

            reasons.append("Bullish Break of Structure")

        # =====================================
        # Bearish Structure
        # =====================================

        elif recent_high < previous_high and recent_low < previous_low:

            structure = "Bearish"

            bos = True

            score = 90

            reasons.append("Lower High created")

            reasons.append("Lower Low created")

            reasons.append("Bearish Break of Structure")

        # =====================================
        # CHOCH Detection
        # =====================================

        if recent_high > previous_high and recent_low < previous_low:

            choch = True

            structure = "Transition"

            score = 65

            reasons.append("Possible Change of Character")

        if len(reasons) == 0:

            reasons.append("Market is currently ranging.")

        return {

            "structure": structure,

            "bos": bos,

            "choch": choch,

            "recent_high": recent_high,

            "recent_low": recent_low,

            "previous_high": previous_high,

            "previous_low": previous_low,

            "score": score,

            "reason": reasons[0],

            "reasons": reasons

        }