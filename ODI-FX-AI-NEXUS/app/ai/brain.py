"""
ODI FX AI NEXUS

AI Brain V1
"""


class AIBrain:

    def __init__(self):

        self.version = "1.0"

    def think(
        self,
        market,
        trend,
        indicators,
        structure,
        support_resistance,
        liquidity,
        order_block,
        fvg,
        mtf,
        signal
    ):

        score = 0

        reasons = []

        # ======================================
        # TREND
        # ======================================

        score += trend["score"] * 0.20

        reasons.extend(trend["reasons"])

        # ======================================
        # MARKET STRUCTURE
        # ======================================

        score += structure["score"] * 0.15

        reasons.extend(structure["reasons"])

        # ======================================
        # SUPPORT / RESISTANCE
        # ======================================

        score += support_resistance["score"] * 0.10

        reasons.append(support_resistance["reason"])

        # ======================================
        # LIQUIDITY
        # ======================================

        score += liquidity["score"] * 0.10

        reasons.append(liquidity["reason"])

        # ======================================
        # ORDER BLOCK
        # ======================================

        score += order_block["score"] * 0.10

        reasons.append(order_block["reason"])

        # ======================================
        # FAIR VALUE GAP
        # ======================================

        score += fvg["score"] * 0.10

        reasons.append(fvg["reason"])

        # ======================================
        # MULTI-TIMEFRAME
        # ======================================

        score += mtf["score"] * 0.15

        reasons.append(mtf["reason"])

        # ======================================
        # SIGNAL ENGINE
        # ======================================

        score += signal["confidence"] * 0.10

        reasons.extend(signal["reasons"])

        # ======================================
        # NORMALISE SCORE
        # ======================================

        confidence = max(0, min(100, round(score)))

        # ======================================
        # TRADE GRADE
        # ======================================

        if confidence >= 95:

            grade = "A+"

        elif confidence >= 90:

            grade = "A"

        elif confidence >= 80:

            grade = "B"

        elif confidence >= 70:

            grade = "C"

        else:

            grade = "NO TRADE"

        # ======================================
        # FINAL DECISION
        # ======================================

        if confidence >= 80:

            decision = signal["signal"]

        else:

            decision = "WAIT"

        # ======================================
        # REMOVE DUPLICATE REASONS
        # ======================================

        unique_reasons = []

        for reason in reasons:

            if reason not in unique_reasons:

                unique_reasons.append(reason)

        # ======================================
        # RETURN AI DECISION
        # ======================================

        return {

            "signal": decision,

            "grade": grade,

            "confidence": confidence,

            "entry_low": signal["entry_low"],

            "entry_high": signal["entry_high"],

            "sl": signal["sl"],

            "tp1": signal["tp1"],

            "tp2": signal["tp2"],

            "tp3": signal["tp3"],

            "rr": signal["rr"],

            "reasons": unique_reasons

        }