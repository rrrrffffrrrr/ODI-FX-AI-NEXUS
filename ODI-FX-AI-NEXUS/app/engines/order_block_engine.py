"""
ODI FX AI NEXUS

Order Block Engine V1
"""


class OrderBlockEngine:

    def __init__(self):
        pass

    def analyse(self, market):

        candles = market["candles"]

        current_price = market["price"]

        bullish_block = None
        bearish_block = None

        # =====================================
        # SEARCH FOR ORDER BLOCKS
        # =====================================

        for i in range(len(candles) - 3, 5, -1):

            candle = candles[i]

            previous = candles[i - 1]

            # -----------------------------
            # Bullish Order Block
            # -----------------------------

            if (

                previous["close"] < previous["open"]

                and

                candle["close"] > previous["high"]

            ):

                bullish_block = {

                    "high": previous["high"],

                    "low": previous["low"]

                }

                break

        for i in range(len(candles) - 3, 5, -1):

            candle = candles[i]

            previous = candles[i - 1]

            # -----------------------------
            # Bearish Order Block
            # -----------------------------

            if (

                previous["close"] > previous["open"]

                and

                candle["close"] < previous["low"]

            ):

                bearish_block = {

                    "high": previous["high"],

                    "low": previous["low"]

                }

                break

        # =====================================
        # DETERMINE ACTIVE BLOCK
        # =====================================

        if bullish_block:

            active = (
                bullish_block["low"]
                <= current_price
                <= bullish_block["high"]
            )

            return {

                "type": "Bullish",

                "high": round(bullish_block["high"], 2),

                "low": round(bullish_block["low"], 2),

                "active": active,

                "mitigated": not active,

                "score": 90 if active else 75,

                "reason": (
                    "Price is trading inside a bullish order block."
                    if active
                    else "Bullish order block identified."
                )

            }

        if bearish_block:

            active = (
                bearish_block["low"]
                <= current_price
                <= bearish_block["high"]
            )

            return {

                "type": "Bearish",

                "high": round(bearish_block["high"], 2),

                "low": round(bearish_block["low"], 2),

                "active": active,

                "mitigated": not active,

                "score": 90 if active else 75,

                "reason": (
                    "Price is trading inside a bearish order block."
                    if active
                    else "Bearish order block identified."
                )

            }

        # =====================================
        # NONE FOUND
        # =====================================

        return {

            "type": "None",

            "high": None,

            "low": None,

            "active": False,

            "mitigated": False,

            "score": 40,

            "reason": "No valid order block detected."

        }