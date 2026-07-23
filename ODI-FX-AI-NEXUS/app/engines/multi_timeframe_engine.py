"""
ODI FX AI NEXUS
Multi-Timeframe Engine
"""


class MultiTimeframeEngine:

    def analyse(self, market):

        candles = market.get("candles", [])
        current_price = float(market.get("price", 0))

        closes = [
            float(candle["close"])
            for candle in candles
            if "close" in candle
        ]

        def detect_trend(lookback):

            if not closes:
                return "Neutral"

            available = closes[-min(lookback, len(closes)):]

            average = sum(available) / len(available)

            if current_price > average:
                return "Bullish"

            if current_price < average:
                return "Bearish"

            return "Neutral"

        m1 = detect_trend(5)
        m5 = detect_trend(20)
        m15 = detect_trend(50)
        h1 = detect_trend(100)
        h4 = detect_trend(200)

        timeframes = [m1, m5, m15, h1, h4]

        bullish_count = timeframes.count("Bullish")
        bearish_count = timeframes.count("Bearish")

        if bullish_count >= 4:

            direction = "Bullish"
            alignment = True
            score = 95
            reason = "Four or more timeframes are aligned bullish."

        elif bearish_count >= 4:

            direction = "Bearish"
            alignment = True
            score = 95
            reason = "Four or more timeframes are aligned bearish."

        else:

            direction = "Mixed"
            alignment = False
            score = 60
            reason = "The analysed timeframes are not fully aligned."

        return {
            "M1": m1,
            "M5": m5,
            "M15": m15,
            "H1": h1,
            "H4": h4,
            "direction": direction,
            "alignment": alignment,
            "score": score,
            "reason": reason,
        }