"""
ODI FX AI NEXUS

Liquidity Engine V1
"""


class LiquidityEngine:

    def __init__(self):
        pass

    def analyse(self, market):

        candles = market["candles"]

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        tolerance = 0.30

        equal_highs = []
        equal_lows = []

        # =====================================
        # FIND EQUAL HIGHS
        # =====================================

        for i in range(len(highs) - 1):

            if abs(highs[i] - highs[i + 1]) <= tolerance:

                equal_highs.append(round(highs[i], 2))

        # =====================================
        # FIND EQUAL LOWS
        # =====================================

        for i in range(len(lows) - 1):

            if abs(lows[i] - lows[i + 1]) <= tolerance:

                equal_lows.append(round(lows[i], 2))

        current_price = market["price"]

        buy_side = False
        sell_side = False

        nearest_price = current_price
        nearest_type = "None"

        # =====================================
        # BUY SIDE LIQUIDITY
        # =====================================

        if len(equal_highs) > 0:

            nearest_buy = min(
                equal_highs,
                key=lambda x: abs(x - current_price)
            )

            if nearest_buy > current_price:

                buy_side = True

                nearest_price = nearest_buy

                nearest_type = "Buy-side"

        # =====================================
        # SELL SIDE LIQUIDITY
        # =====================================

        if len(equal_lows) > 0:

            nearest_sell = min(
                equal_lows,
                key=lambda x: abs(x - current_price)
            )

            if abs(nearest_sell - current_price) < abs(nearest_price - current_price):

                sell_side = True

                nearest_price = nearest_sell

                nearest_type = "Sell-side"

        # =====================================
        # SCORE
        # =====================================

        score = 70

        if buy_side or sell_side:

            score = 90

        reason = (
            f"{nearest_type} liquidity detected."
            if nearest_type != "None"
            else "No significant liquidity pools detected."
        )

        return {

            "buy_side": buy_side,

            "sell_side": sell_side,

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "nearest_price": round(nearest_price, 2),

            "nearest_type": nearest_type,

            "score": score,

            "reason": reason

        }