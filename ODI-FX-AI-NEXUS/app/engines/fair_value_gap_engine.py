"""
ODI FX AI NEXUS

Fair Value Gap Engine V1
"""


class FairValueGapEngine:

    def __init__(self):
        pass

    def analyse(self, market):

        candles = market["candles"]

        current_price = market["price"]

        bullish_gap = None
        bearish_gap = None

        # ======================================
        # FIND FAIR VALUE GAPS
        # ======================================

        for i in range(2, len(candles)):

            c1 = candles[i - 2]
            c2 = candles[i - 1]
            c3 = candles[i]

            # ------------------------------
            # Bullish FVG
            # ------------------------------

            if c3["low"] > c1["high"]:

                bullish_gap = {

                    "high": c3["low"],

                    "low": c1["high"]

                }

            # ------------------------------
            # Bearish FVG
            # ------------------------------

            elif c3["high"] < c1["low"]:

                bearish_gap = {

                    "high": c1["low"],

                    "low": c3["high"]

                }

        # ======================================
        # BULLISH GAP
        # ======================================

        if bullish_gap:

            filled = current_price <= bullish_gap["low"]

            return {

                "direction": "Bullish",

                "high": round(bullish_gap["high"], 2),

                "low": round(bullish_gap["low"], 2),

                "filled": filled,

                "active": not filled,

                "score": 90 if not filled else 70,

                "reason": (
                    "Active bullish Fair Value Gap detected."
                    if not filled
                    else "Bullish Fair Value Gap has been filled."
                )

            }

        # ======================================
        # BEARISH GAP
        # ======================================

        if bearish_gap:

            filled = current_price >= bearish_gap["high"]

            return {

                "direction": "Bearish",

                "high": round(bearish_gap["high"], 2),

                "low": round(bearish_gap["low"], 2),

                "filled": filled,

                "active": not filled,

                "score": 90 if not filled else 70,

                "reason": (
                    "Active bearish Fair Value Gap detected."
                    if not filled
                    else "Bearish Fair Value Gap has been filled."
                )

            }

        # ======================================
        # NONE FOUND
        # ======================================

        return {

            "direction": "None",

            "high": None,

            "low": None,

            "filled": False,

            "active": False,

            "score": 40,

            "reason": "No Fair Value Gap detected."

        }