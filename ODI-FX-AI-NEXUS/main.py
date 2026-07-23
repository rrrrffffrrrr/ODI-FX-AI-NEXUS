"""
ODI FX AI NEXUS

Main Controller
"""

from market_data import get_market_data

from engines.indicator_engine import IndicatorEngine
from engines.trend_engine import TrendEngine
from engines.market_structure_engine import MarketStructureEngine
from engines.support_resistance_engine import SupportResistanceEngine
from engines.liquidity_engine import LiquidityEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fair_value_gap_engine import FairValueGapEngine
from engines.multi_timeframe_engine import MultiTimeframeEngine

from signals.signal_engine import SignalEngine

from ai.brain import AIBrain


def run_ai():

    # ==============================
    # MARKET DATA
    # ==============================

    market = get_market_data()

    # ==============================
    # ENGINES
    # ==============================

    indicator_engine = IndicatorEngine()
    indicators = indicator_engine.analyse(market)

    trend_engine = TrendEngine()
    trend = trend_engine.analyse(
        market,
        indicators
    )

    structure_engine = MarketStructureEngine()
    structure = structure_engine.analyse(market)

    sr_engine = SupportResistanceEngine()
    support_resistance = sr_engine.analyse(market)

    liquidity_engine = LiquidityEngine()
    liquidity = liquidity_engine.analyse(market)

    order_block_engine = OrderBlockEngine()
    order_block = order_block_engine.analyse(market)

    fvg_engine = FairValueGapEngine()
    fvg = fvg_engine.analyse(market)

    mtf_engine = MultiTimeframeEngine()
    mtf = mtf_engine.analyse(market)

    signal_engine = SignalEngine()

    signal = signal_engine.generate(
        market,
        trend,
        indicators,
        structure,
        support_resistance,
        liquidity,
        order_block,
        fvg,
        mtf
    )

    brain = AIBrain()

    ai = brain.think(
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
    )

    return {

        "market": market,

        "indicators": indicators,

        "trend": trend,

        "structure": structure,

        "support_resistance": support_resistance,

        "liquidity": liquidity,

        "order_block": order_block,

        "fvg": fvg,

        "mtf": mtf,

        "signal": signal,

        "ai": ai

    }