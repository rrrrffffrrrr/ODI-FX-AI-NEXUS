"""
ODI FX AI NEXUS

Support & Resistance Engine V1
"""


class SupportResistanceEngine:

    def __init__(self):
        pass

    def analyse(self, market):

        candles = market["candles"]

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        # ======================================
        # LOOKBACK
        # ======================================

        recent_highs = highs[-100:]
        recent_lows = lows[-100:]

        resistance = round(max(recent_highs), 2)
        support = round(min(recent_lows), 2)

        current_price = market["price"]

        range_size = round(resistance - support, 2)

        distance_to_support = round(
            current_price - support,
            2
        )

        distance_to_resistance = round(
            resistance - current_price,
            2
        )

        # ======================================
        # MARKET POSITION
        # ======================================

        if distance_to_support < distance_to_resistance:

            position = "Near Support"

            score = 85

            reason = "Price is trading close to support."

        elif distance_to_resistance < distance_to_support:

            position = "Near Resistance"

            score = 85

            reason = "Price is trading close to resistance."

        else:

            position = "Middle of Range"

            score = 60

            reason = "Price is trading between major levels."

        return {

            "support": support,

            "resistance": resistance,

            "range": range_size,

            "current_price": current_price,

            "distance_to_support": distance_to_support,

            "distance_to_resistance": distance_to_resistance,

            "position": position,

            "score": score,

            "reason": reason

        }