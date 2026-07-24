"""
ODI FX AI NEXUS

Connected AI Trading Dashboard
"""

import html

import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

from config import APP_NAME, VERSION, AI_STATUS
from main import run_ai


def render_html(body, *args, **kwargs):
    """Render indented HTML without showing it as code."""

    if isinstance(body, str):
        body = "\n".join(
            line.lstrip()
            for line in body.splitlines()
        ).strip()

    return st.markdown(
        body,
        *args,
        **kwargs,
    )

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st_autorefresh(
    interval=10_000,
    key="nexus_refresh",
)


# ==================================================
# LOAD COMPLETE AI ANALYSIS
# ==================================================

try:
    result = run_ai()

except Exception as error:
    st.error("ODI FX AI NEXUS could not complete its market analysis.")
    st.exception(error)
    st.stop()


market = result["market"]
indicators = result["indicators"]
trend = result["trend"]
structure = result["structure"]
support_resistance = result["support_resistance"]
liquidity = result["liquidity"]
order_block = result["order_block"]
fvg = result["fvg"]
mtf = result["mtf"]
signal = result["signal"]
ai = result["ai"]


# ==================================================
# DISPLAY HELPERS
# ==================================================

def safe_text(value, fallback="-"):
    """Safely format values for the dashboard."""

    if value is None:
        return fallback

    return html.escape(str(value))


def price_text(value):
    """Format a market price to two decimal places."""

    if isinstance(value, (int, float)):
        return f"{value:,.2f}"

    return safe_text(value)


def decision_colour(decision):
    """Return the interface colour for an AI decision."""

    colours = {
        "BUY": "#00F0A8",
        "SELL": "#FF4D6D",
        "WAIT": "#FFD166",
        "NO TRADE": "#FFD166",
    }

    return colours.get(str(decision).upper(), "#7FDBFF")


def state_colour(state):
    """Return a colour for bullish, bearish or neutral states."""

    state = str(state).lower()

    if any(word in state for word in ("bullish", "buy", "high", "online", "active")):
        return "#00F0A8"

    if any(word in state for word in ("bearish", "sell", "low", "offline")):
        return "#FF4D6D"

    return "#FFD166"


decision = ai.get("signal", "WAIT")
decision_hex = decision_colour(decision)


# ==================================================
# NEXUS VISUAL SYSTEM
# ==================================================

render_html(
    f"""
    <style>
    :root {{
        --nexus-bg: #02040d;
        --nexus-panel: rgba(8, 18, 38, 0.72);
        --nexus-panel-light: rgba(12, 29, 58, 0.68);
        --nexus-border: rgba(87, 215, 255, 0.20);
        --nexus-cyan: #57d7ff;
        --nexus-blue: #388bff;
        --nexus-gold: #ffd166;
        --nexus-green: #00f0a8;
        --nexus-red: #ff4d6d;
        --nexus-text: #f4f8ff;
        --nexus-muted: #91a8c8;
        --decision-colour: {decision_hex};
    }}

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {{
        background:
            radial-gradient(
                circle at 16% 8%,
                rgba(37, 94, 190, 0.32) 0%,
                transparent 34%
            ),
            radial-gradient(
                circle at 88% 16%,
                rgba(0, 204, 255, 0.18) 0%,
                transparent 30%
            ),
            radial-gradient(
                circle at 52% 108%,
                rgba(94, 58, 180, 0.24) 0%,
                transparent 38%
            ),
            linear-gradient(
                155deg,
                #02040d 0%,
                #061125 48%,
                #02040d 100%
            );
        color: var(--nexus-text);
    }}

    [data-testid="stAppViewContainer"] {{
        overflow-x: hidden;
    }}

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer {{
        visibility: hidden;
        height: 0;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(3, 10, 24, 0.94);
        border-right: 1px solid var(--nexus-border);
    }}

    .main .block-container {{
        max-width: 1700px;
        padding-top: 1.1rem;
        padding-bottom: 3rem;
    }}

    /* Animated space layers */

    .nexus-space,
    .nexus-space::before,
    .nexus-space::after {{
        position: fixed;
        inset: 0;
        content: "";
        pointer-events: none;
    }}

    .nexus-space {{
        z-index: 0;
        opacity: 0.58;
        background-image:
            radial-gradient(circle, rgba(255,255,255,0.95) 1px, transparent 1.5px),
            radial-gradient(circle, rgba(91,210,255,0.80) 1px, transparent 1.5px);
        background-size: 78px 78px, 126px 126px;
        background-position: 0 0, 34px 27px;
        animation: nexusStarsNear 95s linear infinite;
    }}

    .nexus-space::before {{
        opacity: 0.40;
        background-image:
            radial-gradient(circle, rgba(255,255,255,0.75) 1px, transparent 1.4px);
        background-size: 44px 44px;
        animation: nexusStarsFar 155s linear infinite;
    }}

    .nexus-space::after {{
        opacity: 0.20;
        background:
            radial-gradient(
                ellipse at 75% 18%,
                rgba(58, 174, 255, 0.52),
                transparent 32%
            ),
            radial-gradient(
                ellipse at 18% 70%,
                rgba(119, 70, 210, 0.44),
                transparent 34%
            );
        filter: blur(55px);
        animation: nexusNebula 16s ease-in-out infinite alternate;
    }}

    @keyframes nexusStarsNear {{
        from {{ transform: translate3d(0, 0, 0); }}
        to {{ transform: translate3d(-150px, -900px, 0); }}
    }}

    @keyframes nexusStarsFar {{
        from {{ transform: translate3d(0, 0, 0); }}
        to {{ transform: translate3d(110px, -650px, 0); }}
    }}

    @keyframes nexusNebula {{
        from {{ transform: scale(1) translate3d(0, 0, 0); }}
        to {{ transform: scale(1.12) translate3d(-35px, 24px, 0); }}
    }}

    /* Header */

    .nexus-header {{
        position: relative;
        z-index: 2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 24px;
        padding: 22px 26px;
        margin-bottom: 18px;
        border: 1px solid var(--nexus-border);
        border-radius: 24px;
        background:
            linear-gradient(
                120deg,
                rgba(10, 29, 61, 0.88),
                rgba(4, 12, 29, 0.74)
            );
        box-shadow:
            0 20px 55px rgba(0, 0, 0, 0.34),
            inset 0 1px 0 rgba(255,255,255,0.05),
            0 0 34px rgba(52, 178, 255, 0.09);
        backdrop-filter: blur(20px);
    }}

    .nexus-title {{
        margin: 0;
        font-size: clamp(29px, 4vw, 48px);
        line-height: 1;
        letter-spacing: 0.04em;
        font-weight: 800;
        color: #ffffff;
        text-shadow:
            0 0 12px rgba(87, 215, 255, 0.60),
            0 0 34px rgba(56, 139, 255, 0.35);
    }}

    .nexus-subtitle {{
        margin-top: 10px;
        color: var(--nexus-muted);
        font-size: 14px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }}

    .nexus-live {{
        min-width: 170px;
        padding: 12px 16px;
        text-align: center;
        color: var(--nexus-green);
        border: 1px solid rgba(0, 240, 168, 0.28);
        border-radius: 999px;
        background: rgba(0, 240, 168, 0.07);
        box-shadow: 0 0 28px rgba(0, 240, 168, 0.10);
        font-weight: 700;
        letter-spacing: 0.08em;
    }}

    .nexus-live-dot {{
        display: inline-block;
        width: 9px;
        height: 9px;
        margin-right: 8px;
        border-radius: 50%;
        background: var(--nexus-green);
        box-shadow: 0 0 14px var(--nexus-green);
        animation: nexusLivePulse 1.7s ease-in-out infinite;
    }}

    @keyframes nexusLivePulse {{
        0%, 100% {{ opacity: 0.45; transform: scale(0.9); }}
        50% {{ opacity: 1; transform: scale(1.2); }}
    }}

    /* Reusable panels */

    .nexus-panel {{
        position: relative;
        z-index: 2;
        height: 100%;
        padding: 20px;
        border: 1px solid var(--nexus-border);
        border-radius: 22px;
        background:
            linear-gradient(
                145deg,
                var(--nexus-panel-light),
                var(--nexus-panel)
            );
        box-shadow:
            0 18px 45px rgba(0,0,0,0.28),
            inset 0 1px 0 rgba(255,255,255,0.04);
        backdrop-filter: blur(18px);
    }}

    .nexus-section-title {{
        margin: 8px 0 14px;
        color: #dff7ff;
        font-size: 21px;
        font-weight: 750;
        letter-spacing: 0.02em;
        text-shadow: 0 0 16px rgba(87,215,255,0.20);
    }}

    .nexus-label {{
        color: var(--nexus-muted);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.10em;
        text-transform: uppercase;
    }}

    .nexus-value {{
        margin-top: 6px;
        color: var(--nexus-text);
        font-size: 24px;
        font-weight: 750;
    }}

    /* Streamlit metrics */

    [data-testid="stMetric"] {{
        min-height: 118px;
        padding: 18px 18px 14px;
        border: 1px solid var(--nexus-border);
        border-radius: 20px;
        background:
            linear-gradient(
                145deg,
                rgba(13, 35, 70, 0.76),
                rgba(4, 14, 31, 0.72)
            );
        box-shadow:
            0 16px 40px rgba(0,0,0,0.22),
            0 0 28px rgba(44, 175, 255, 0.07);
        backdrop-filter: blur(16px);
    }}

    [data-testid="stMetricLabel"] {{
        color: var(--nexus-muted);
        letter-spacing: 0.05em;
    }}

    [data-testid="stMetricValue"] {{
        color: #f5fbff;
        text-shadow: 0 0 14px rgba(87,215,255,0.16);
    }}

    /* Alerts */

    [data-testid="stAlert"] {{
        border-radius: 16px;
        border: 1px solid rgba(87,215,255,0.18);
        background: rgba(6, 20, 42, 0.76);
        backdrop-filter: blur(12px);
    }}

    hr {{
        border-color: rgba(87,215,255,0.14);
    }}

    @media (max-width: 900px) {{
        .nexus-header {{
            align-items: flex-start;
            flex-direction: column;
        }}

        .nexus-live {{
            min-width: 0;
        }}
    }}
    </style>

    <div class="nexus-space"></div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# NEXUS HEADER
# ==================================================

render_html(
    f"""
    <div class="nexus-header">
        <div>
            <h1 class="nexus-title">🌌 {safe_text(APP_NAME)}</h1>
            <div class="nexus-subtitle">
                Artificial Intelligence Trading Command Centre
            </div>
        </div>

        <div class="nexus-live">
            <span class="nexus-live-dot"></span>
            XAUUSD LIVE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# ==================================================
# LIVE MARKET METRICS
# ==================================================

metric_1, metric_2, metric_3, metric_4, metric_5 = st.columns(5)

with metric_1:
    st.metric(
        label="XAUUSD Price",
        value=f"${price_text(market.get('price'))}",
    )

with metric_2:
    st.metric(
        label="Bid",
        value=f"${price_text(market.get('bid'))}",
    )

with metric_3:
    st.metric(
        label="Ask",
        value=f"${price_text(market.get('ask'))}",
    )

with metric_4:
    st.metric(
        label="Spread",
        value=price_text(market.get("spread")),
    )

with metric_5:
    st.metric(
        label="Volume",
        value=f"{market.get('volume', 0):,}",
    )


render_html("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==================================================
# DASHBOARD GRID
# ==================================================

chart_column, ai_column = st.columns(
    [1.75, 1],
    gap="large",
)


# ==================================================
# TRADINGVIEW TERMINAL
# ==================================================

with chart_column:

    render_html(
        """
        <div class="nexus-section-title">
            📊 Live Gold Market Terminal
        </div>
        """,
        unsafe_allow_html=True,
    )

    tradingview_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            html,
            body {
                width: 100%;
                height: 100%;
                margin: 0;
                overflow: hidden;
                background: #020711;
                font-family: Arial, sans-serif;
            }

            .terminal-shell {
                width: calc(100% - 2px);
                height: calc(100% - 2px);
                overflow: hidden;
                border: 1px solid rgba(87, 215, 255, 0.24);
                border-radius: 22px;
                background:
                    radial-gradient(
                        circle at 20% 0%,
                        rgba(26, 99, 190, 0.25),
                        transparent 36%
                    ),
                    #020711;
                box-shadow:
                    inset 0 1px 0 rgba(255, 255, 255, 0.04),
                    0 18px 50px rgba(0, 0, 0, 0.40);
            }

            .tradingview-widget-container,
            .tradingview-widget-container__widget {
                width: 100%;
                height: 100%;
            }
        </style>
    </head>

    <body>
        <div class="terminal-shell">
            <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>

                <script
                    type="text/javascript"
                    src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js"
                    async
                >
                {
                    "autosize": true,
                    "symbol": "OANDA:XAUUSD",
                    "interval": "5",
                    "timezone": "Europe/London",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "backgroundColor": "rgba(2, 7, 17, 1)",
                    "gridColor": "rgba(87, 215, 255, 0.06)",
                    "hide_top_toolbar": false,
                    "hide_legend": false,
                    "allow_symbol_change": false,
                    "save_image": false,
                    "calendar": false,
                    "support_host": "https://www.tradingview.com"
                }
                </script>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(
        tradingview_html,
        height=720,
        scrolling=False,
    )


# ==================================================
# AI DECISION COMMAND PANEL
# ==================================================

with ai_column:

    render_html(
        """
        <div class="nexus-section-title">
            🧠 AI Decision Core
        </div>
        """,
        unsafe_allow_html=True,
    )

    sphere_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            html,
            body {{
                width: 100%;
                height: 100%;
                margin: 0;
                overflow: hidden;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .core-shell {{
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 300px;
                overflow: hidden;
                border: 1px solid rgba(87, 215, 255, 0.22);
                border-radius: 22px;
                background:
                    radial-gradient(
                        circle at center,
                        rgba(56, 139, 255, 0.18),
                        transparent 48%
                    ),
                    linear-gradient(
                        145deg,
                        rgba(8, 26, 55, 0.92),
                        rgba(2, 8, 21, 0.96)
                    );
                box-shadow:
                    inset 0 1px 0 rgba(255,255,255,0.05),
                    0 20px 50px rgba(0,0,0,0.32);
            }}

            .core-glow {{
                position: absolute;
                width: 230px;
                height: 230px;
                border-radius: 50%;
                background: radial-gradient(
                    circle,
                    {decision_hex}33 0%,
                    {decision_hex}12 42%,
                    transparent 72%
                );
                filter: blur(7px);
                animation: coreBreathe 2.4s ease-in-out infinite;
            }}

            .core-sphere {{
                position: absolute;
                width: 128px;
                height: 128px;
                border-radius: 50%;
                background:
                    radial-gradient(
                        circle at 35% 28%,
                        #ffffff 0%,
                        {decision_hex} 12%,
                        #1264a3 42%,
                        #04162f 74%
                    );
                box-shadow:
                    0 0 18px {decision_hex},
                    0 0 48px {decision_hex}99,
                    0 0 95px {decision_hex}55,
                    inset -18px -22px 36px rgba(0,0,0,0.68),
                    inset 10px 10px 24px rgba(255,255,255,0.20);
                animation:
                    sphereFloat 4.8s ease-in-out infinite,
                    spherePulse 2.4s ease-in-out infinite;
            }}

            .core-sphere::before {{
                position: absolute;
                inset: 13px;
                content: "";
                border: 1px solid rgba(255,255,255,0.30);
                border-radius: 50%;
                animation: sphereRotate 7s linear infinite;
            }}

            .core-sphere::after {{
                position: absolute;
                top: 22px;
                left: 28px;
                width: 30px;
                height: 17px;
                content: "";
                border-radius: 50%;
                background: rgba(255,255,255,0.62);
                filter: blur(5px);
                transform: rotate(-28deg);
            }}

            .orbit {{
                position: absolute;
                width: 220px;
                height: 84px;
                border: 1px solid {decision_hex}99;
                border-radius: 50%;
                box-shadow: 0 0 14px {decision_hex}55;
            }}

            .orbit-one {{
                transform: rotate(18deg);
                animation: orbitOne 9s linear infinite;
            }}

            .orbit-two {{
                transform: rotate(78deg);
                animation: orbitTwo 7s linear infinite reverse;
            }}

            .orbit-three {{
                width: 178px;
                height: 178px;
                transform: rotateX(68deg);
                animation: orbitThree 12s linear infinite;
            }}

            .core-label {{
                position: absolute;
                bottom: 20px;
                text-align: center;
            }}

            .core-status {{
                color: {decision_hex};
                font-size: 26px;
                font-weight: 800;
                letter-spacing: 0.14em;
                text-shadow: 0 0 20px {decision_hex};
            }}

            .core-caption {{
                margin-top: 6px;
                color: #91a8c8;
                font-size: 11px;
                letter-spacing: 0.15em;
                text-transform: uppercase;
            }}

            @keyframes coreBreathe {{
                0%, 100% {{
                    opacity: 0.55;
                    transform: scale(0.92);
                }}

                50% {{
                    opacity: 1;
                    transform: scale(1.12);
                }}
            }}

            @keyframes sphereFloat {{
                0%, 100% {{
                    transform: translateY(-5px);
                }}

                50% {{
                    transform: translateY(8px);
                }}
            }}

            @keyframes spherePulse {{
                0%, 100% {{
                    filter: brightness(0.88);
                }}

                50% {{
                    filter: brightness(1.25);
                }}
            }}

            @keyframes sphereRotate {{
                from {{
                    transform: rotate(0deg);
                }}

                to {{
                    transform: rotate(360deg);
                }}
            }}

            @keyframes orbitOne {{
                from {{
                    transform: rotate(18deg) rotateZ(0deg);
                }}

                to {{
                    transform: rotate(18deg) rotateZ(360deg);
                }}
            }}

            @keyframes orbitTwo {{
                from {{
                    transform: rotate(78deg) rotateZ(0deg);
                }}

                to {{
                    transform: rotate(78deg) rotateZ(360deg);
                }}
            }}

            @keyframes orbitThree {{
                from {{
                    transform: rotateX(68deg) rotateZ(0deg);
                }}

                to {{
                    transform: rotateX(68deg) rotateZ(360deg);
                }}
            }}
        </style>
    </head>

    <body>
        <div class="core-shell">
            <div class="core-glow"></div>
            <div class="orbit orbit-one"></div>
            <div class="orbit orbit-two"></div>
            <div class="orbit orbit-three"></div>
            <div class="core-sphere"></div>

            <div class="core-label">
                <div class="core-status">
                    {safe_text(decision)}
                </div>

                <div class="core-caption">
                    Nexus Intelligence Core
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(
        sphere_html,
        height=302,
        scrolling=False,
    )

    render_html(
        f"""
        <div class="nexus-panel" style="margin-top: 14px;">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 14px;
                margin-bottom: 18px;
            ">
                <div>
                    <div class="nexus-label">Final AI Decision</div>

                    <div style="
                        margin-top: 7px;
                        color: {decision_hex};
                        font-size: 35px;
                        font-weight: 850;
                        letter-spacing: 0.08em;
                        text-shadow: 0 0 20px {decision_hex}88;
                    ">
                        {safe_text(decision)}
                    </div>
                </div>

                <div style="
                    min-width: 84px;
                    padding: 12px;
                    text-align: center;
                    border: 1px solid {decision_hex}55;
                    border-radius: 17px;
                    background: {decision_hex}12;
                ">
                    <div class="nexus-label">Grade</div>

                    <div style="
                        margin-top: 5px;
                        color: {decision_hex};
                        font-size: 25px;
                        font-weight: 800;
                    ">
                        {safe_text(ai.get("grade"))}
                    </div>
                </div>
            </div>

            <div style="
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
            ">
                <div style="
                    padding: 13px;
                    border: 1px solid rgba(87,215,255,0.16);
                    border-radius: 15px;
                    background: rgba(0,0,0,0.16);
                ">
                    <div class="nexus-label">Confidence</div>
                    <div class="nexus-value">
                        {safe_text(ai.get("confidence", 0))}%
                    </div>
                </div>

                <div style="
                    padding: 13px;
                    border: 1px solid rgba(87,215,255,0.16);
                    border-radius: 15px;
                    background: rgba(0,0,0,0.16);
                ">
                    <div class="nexus-label">Risk : Reward</div>
                    <div class="nexus-value">
                        {safe_text(ai.get("rr"))}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# TRADE LEVELS
# ==================================================

render_html(
    """
    <div class="nexus-section-title" style="margin-top: 24px;">
        🎯 AI Trade Levels
    </div>
    """,
    unsafe_allow_html=True,
)

level_1, level_2, level_3, level_4, level_5, level_6 = st.columns(6)

with level_1:
    st.metric(
        label="Entry Low",
        value=price_text(ai.get("entry_low")),
    )

with level_2:
    st.metric(
        label="Entry High",
        value=price_text(ai.get("entry_high")),
    )

with level_3:
    st.metric(
        label="Stop Loss",
        value=price_text(ai.get("sl")),
    )

with level_4:
    st.metric(
        label="Take Profit 1",
        value=price_text(ai.get("tp1")),
    )

with level_5:
    st.metric(
        label="Take Profit 2",
        value=price_text(ai.get("tp2")),
    )

with level_6:
    st.metric(
        label="Take Profit 3",
        value=price_text(ai.get("tp3")),
    )
    # ==================================================
# ANALYSIS PANEL HELPERS
# ==================================================

def first_value(data, *keys, fallback="-"):
    """Return the first available value from several possible keys."""

    for key in keys:
        value = data.get(key)

        if value is not None:
            return value

    return fallback


def yes_no(value):
    """Format boolean values for display."""

    return "YES" if value else "NO"


def format_reason(data):
    """Format one or several engine reasons."""

    reasons = data.get("reasons")

    if isinstance(reasons, list) and reasons:
        return " • ".join(str(reason) for reason in reasons)

    return data.get("reason", "No additional reasoning available.")


def render_analysis_panel(
    title,
    icon,
    state,
    rows,
    reason,
):
    """Render one reusable AI analysis panel."""

    accent = state_colour(state)

    row_html = ""

    for label, value in rows:
        row_html += f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 11px 0;
            border-bottom: 1px solid rgba(87,215,255,0.10);
        ">
            <span class="nexus-label">
                {safe_text(label)}
            </span>

            <span style="
                color: #f4f8ff;
                font-size: 15px;
                font-weight: 700;
                text-align: right;
            ">
                {safe_text(value)}
            </span>
        </div>
        """

    render_html(
        f"""
        <div class="nexus-panel" style="margin-bottom: 18px;">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 14px;
                margin-bottom: 12px;
            ">
                <div style="
                    color: #dff7ff;
                    font-size: 19px;
                    font-weight: 800;
                ">
                    {safe_text(icon)} {safe_text(title)}
                </div>

                <div style="
                    padding: 7px 11px;
                    color: {accent};
                    font-size: 12px;
                    font-weight: 800;
                    letter-spacing: 0.08em;
                    border: 1px solid {accent}55;
                    border-radius: 999px;
                    background: {accent}12;
                    text-transform: uppercase;
                ">
                    {safe_text(state)}
                </div>
            </div>

            <div>
                {row_html}
            </div>

            <div style="
                margin-top: 15px;
                padding: 13px;
                color: #a9bdd8;
                font-size: 13px;
                line-height: 1.55;
                border-left: 3px solid {accent};
                border-radius: 8px;
                background: rgba(0,0,0,0.16);
            ">
                {safe_text(reason)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# ENGINE ANALYSIS HEADER
# ==================================================

render_html(
    """
    <div class="nexus-section-title" style="margin-top: 26px;">
        🔬 Nexus Intelligence Analysis
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# TREND AND INDICATORS
# ==================================================

analysis_left, analysis_right = st.columns(
    2,
    gap="large",
)

with analysis_left:

    trend_state = first_value(
        trend,
        "trend",
        "direction",
        fallback="Neutral",
    )

    render_analysis_panel(
        title="Trend Engine",
        icon="📈",
        state=trend_state,
        rows=[
            (
                "Direction",
                trend_state,
            ),
            (
                "Trend Score",
                first_value(
                    trend,
                    "score",
                    fallback=0,
                ),
            ),
            (
                "Strength",
                first_value(
                    trend,
                    "strength",
                    "trend_strength",
                    fallback="-",
                ),
            ),
            (
                "Current Price",
                price_text(market.get("price")),
            ),
        ],
        reason=format_reason(trend),
    )

with analysis_right:

    ema_state = first_value(
        indicators,
        "ema",
        "ema_bias",
        "bias",
        fallback="Neutral",
    )

    render_analysis_panel(
        title="Indicator Engine",
        icon="📊",
        state=ema_state,
        rows=[
            (
                "EMA Bias",
                ema_state,
            ),
            (
                "Fast EMA",
                price_text(
                    first_value(
                        indicators,
                        "fast_ema",
                        "ema_fast",
                        "ema20",
                    )
                ),
            ),
            (
                "Slow EMA",
                price_text(
                    first_value(
                        indicators,
                        "slow_ema",
                        "ema_slow",
                        "ema50",
                    )
                ),
            ),
            (
                "RSI",
                first_value(
                    indicators,
                    "rsi",
                    fallback="-",
                ),
            ),
            (
                "Momentum",
                first_value(
                    indicators,
                    "momentum",
                    "rsi_state",
                    fallback="-",
                ),
            ),
            (
                "Volume",
                first_value(
                    indicators,
                    "volume",
                    "volume_state",
                    fallback="-",
                ),
            ),
            (
                "MACD",
                first_value(
                    indicators,
                    "macd",
                    fallback="Coming Soon",
                ),
            ),
        ],
        reason=first_value(
            indicators,
            "reason",
            fallback="Technical indicators analysed successfully.",
        ),
    )


# ==================================================
# MARKET STRUCTURE AND SUPPORT / RESISTANCE
# ==================================================

structure_column, levels_column = st.columns(
    2,
    gap="large",
)

with structure_column:

    structure_state = first_value(
        structure,
        "structure",
        "direction",
        fallback="Neutral",
    )

    render_analysis_panel(
        title="Market Structure",
        icon="🏛️",
        state=structure_state,
        rows=[
            (
                "Structure",
                structure_state,
            ),
            (
                "Break of Structure",
                yes_no(
                    first_value(
                        structure,
                        "bos",
                        fallback=False,
                    )
                ),
            ),
            (
                "Change of Character",
                yes_no(
                    first_value(
                        structure,
                        "choch",
                        fallback=False,
                    )
                ),
            ),
            (
                "Recent High",
                price_text(
                    first_value(
                        structure,
                        "recent_high",
                        fallback="-",
                    )
                ),
            ),
            (
                "Recent Low",
                price_text(
                    first_value(
                        structure,
                        "recent_low",
                        fallback="-",
                    )
                ),
            ),
            (
                "Structure Score",
                first_value(
                    structure,
                    "score",
                    fallback=0,
                ),
            ),
        ],
        reason=format_reason(structure),
    )

with levels_column:

    level_state = first_value(
        support_resistance,
        "position",
        fallback="Range",
    )

    render_analysis_panel(
        title="Support & Resistance",
        icon="📐",
        state=level_state,
        rows=[
            (
                "Support",
                price_text(
                    support_resistance.get("support")
                ),
            ),
            (
                "Resistance",
                price_text(
                    support_resistance.get("resistance")
                ),
            ),
            (
                "Range Size",
                price_text(
                    support_resistance.get("range")
                ),
            ),
            (
                "Distance to Support",
                price_text(
                    support_resistance.get(
                        "distance_to_support"
                    )
                ),
            ),
            (
                "Distance to Resistance",
                price_text(
                    support_resistance.get(
                        "distance_to_resistance"
                    )
                ),
            ),
            (
                "Level Score",
                support_resistance.get("score", 0),
            ),
        ],
        reason=format_reason(support_resistance),
    )


# ==================================================
# LIQUIDITY AND ORDER BLOCKS
# ==================================================

liquidity_column, order_block_column = st.columns(
    2,
    gap="large",
)

with liquidity_column:

    liquidity_state = first_value(
        liquidity,
        "nearest_type",
        fallback="None",
    )

    equal_highs = liquidity.get("equal_highs", [])
    equal_lows = liquidity.get("equal_lows", [])

    render_analysis_panel(
        title="Liquidity Engine",
        icon="💧",
        state=liquidity_state,
        rows=[
            (
                "Nearest Pool",
                liquidity_state,
            ),
            (
                "Liquidity Price",
                price_text(
                    liquidity.get("nearest_price")
                ),
            ),
            (
                "Buy-Side Liquidity",
                yes_no(
                    liquidity.get("buy_side", False)
                ),
            ),
            (
                "Sell-Side Liquidity",
                yes_no(
                    liquidity.get("sell_side", False)
                ),
            ),
            (
                "Equal Highs",
                len(equal_highs),
            ),
            (
                "Equal Lows",
                len(equal_lows),
            ),
            (
                "Liquidity Score",
                liquidity.get("score", 0),
            ),
        ],
        reason=format_reason(liquidity),
    )

with order_block_column:

    order_block_state = first_value(
        order_block,
        "type",
        fallback="None",
    )

    render_analysis_panel(
        title="Order Block Engine",
        icon="📦",
        state=order_block_state,
        rows=[
            (
                "Block Type",
                order_block_state,
            ),
            (
                "Zone High",
                price_text(
                    order_block.get("high")
                ),
            ),
            (
                "Zone Low",
                price_text(
                    order_block.get("low")
                ),
            ),
            (
                "Active",
                yes_no(
                    order_block.get("active", False)
                ),
            ),
            (
                "Mitigated",
                yes_no(
                    order_block.get("mitigated", False)
                ),
            ),
            (
                "Block Score",
                order_block.get("score", 0),
            ),
        ],
        reason=format_reason(order_block),
    )


# ==================================================
# FAIR VALUE GAP AND MULTI-TIMEFRAME
# ==================================================

fvg_column, mtf_column = st.columns(
    2,
    gap="large",
)

with fvg_column:

    fvg_state = first_value(
        fvg,
        "direction",
        fallback="None",
    )

    render_analysis_panel(
        title="Fair Value Gap",
        icon="⚡",
        state=fvg_state,
        rows=[
            (
                "Direction",
                fvg_state,
            ),
            (
                "Gap High",
                price_text(
                    fvg.get("high")
                ),
            ),
            (
                "Gap Low",
                price_text(
                    fvg.get("low")
                ),
            ),
            (
                "Active",
                yes_no(
                    fvg.get("active", False)
                ),
            ),
            (
                "Filled",
                yes_no(
                    fvg.get("filled", False)
                ),
            ),
            (
                "FVG Score",
                fvg.get("score", 0),
            ),
        ],
        reason=format_reason(fvg),
    )

with mtf_column:

    mtf_state = first_value(
        mtf,
        "direction",
        fallback="Mixed",
    )

    render_analysis_panel(
        title="Multi-Timeframe Alignment",
        icon="⏱️",
        state=mtf_state,
        rows=[
            (
                "M1",
                mtf.get("M1", "Neutral"),
            ),
            (
                "M5",
                mtf.get("M5", "Neutral"),
            ),
            (
                "M15",
                mtf.get("M15", "Neutral"),
            ),
            (
                "H1",
                mtf.get("H1", "Neutral"),
            ),
            (
                "H4",
                mtf.get("H4", "Neutral"),
            ),
            (
                "Aligned",
                yes_no(
                    mtf.get("alignment", False)
                ),
            ),
            (
                "Alignment Score",
                mtf.get("score", 0),
            ),
        ],
        reason=format_reason(mtf),
    )
    # ==================================================
# AI REASONING
# ==================================================

render_html(
    """
    <div class="nexus-section-title" style="margin-top: 26px;">
        🧠 AI Decision Reasoning
    </div>
    """,
    unsafe_allow_html=True,
)

reasoning_column, status_column = st.columns(
    [1.6, 1],
    gap="large",
)

with reasoning_column:

    ai_reasons = ai.get("reasons", [])

    if not isinstance(ai_reasons, list):
        ai_reasons = [str(ai_reasons)]

    if ai_reasons:

        reasoning_html = ""

        for number, reason in enumerate(ai_reasons, start=1):

            reasoning_html += f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 13px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex: 0 0 31px;
                    width: 31px;
                    height: 31px;
                    color: {decision_hex};
                    font-size: 12px;
                    font-weight: 800;
                    border: 1px solid {decision_hex}55;
                    border-radius: 50%;
                    background: {decision_hex}12;
                    box-shadow: 0 0 16px {decision_hex}22;
                ">
                    {number}
                </div>

                <div style="
                    padding-top: 4px;
                    color: #c7d8ed;
                    font-size: 14px;
                    line-height: 1.55;
                ">
                    {safe_text(reason)}
                </div>
            </div>
            """

    else:

        reasoning_html = """
        <div style="
            padding: 18px 0;
            color: #91a8c8;
            font-size: 14px;
        ">
            No AI reasoning is currently available.
        </div>
        """

    render_html(
        f"""
        <div class="nexus-panel">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            ">
                <div style="
                    color: #dff7ff;
                    font-size: 19px;
                    font-weight: 800;
                ">
                    Neural Decision Evidence
                </div>

                <div style="
                    padding: 7px 11px;
                    color: {decision_hex};
                    font-size: 12px;
                    font-weight: 800;
                    border: 1px solid {decision_hex}55;
                    border-radius: 999px;
                    background: {decision_hex}12;
                ">
                    {len(ai_reasons)} REASONS
                </div>
            </div>

            {reasoning_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# SYSTEM STATUS
# ==================================================

with status_column:

    system_online = str(AI_STATUS).upper() == "ONLINE"

    system_colour = (
        "#00F0A8"
        if system_online
        else "#FF4D6D"
    )

    refresh_time = market.get(
        "time",
        "Awaiting update",
    )

    render_html(
        f"""
        <div class="nexus-panel">
            <div style="
                color: #dff7ff;
                font-size: 19px;
                font-weight: 800;
                margin-bottom: 16px;
            ">
                ⚙️ System Status
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <span class="nexus-label">
                    AI Core
                </span>

                <span style="
                    color: {system_colour};
                    font-weight: 800;
                ">
                    ● {safe_text(AI_STATUS)}
                </span>
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <span class="nexus-label">
                    Platform Version
                </span>

                <span style="
                    color: #f4f8ff;
                    font-weight: 700;
                ">
                    {safe_text(VERSION)}
                </span>
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <span class="nexus-label">
                    Market
                </span>

                <span style="
                    color: #f4f8ff;
                    font-weight: 700;
                ">
                    {safe_text(market.get("symbol", "XAUUSD"))}
                </span>
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <span class="nexus-label">
                    Data Mode
                </span>

                <span style="
                    color: #FFD166;
                    font-weight: 700;
                ">
                {safe_text(market.get("data_mode", "LIVE"))} 
                </span>
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(87,215,255,0.10);
            ">
                <span class="nexus-label">
                    Refresh Rate
                </span>

                <span style="
                    color: #f4f8ff;
                    font-weight: 700;
                ">
                    10 seconds
                </span>
            </div>

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 13px 0 0;
            ">
                <span class="nexus-label">
                    Last Analysis
                </span>

                <span style="
                    color: #f4f8ff;
                    font-size: 13px;
                    font-weight: 700;
                    text-align: right;
                ">
                    {safe_text(refresh_time)}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# SIGNAL ENGINE SUMMARY
# ==================================================

render_html(
    """
    <div class="nexus-section-title" style="margin-top: 26px;">
        📡 Signal Engine Summary
    </div>
    """,
    unsafe_allow_html=True,
)

signal_1, signal_2, signal_3, signal_4 = st.columns(4)

with signal_1:
    st.metric(
        label="Raw Signal",
        value=safe_text(
            signal.get("signal", "WAIT")
        ),
    )

with signal_2:
    st.metric(
        label="Raw Score",
        value=signal.get("score", 0),
    )

with signal_3:
    st.metric(
        label="Signal Confidence",
        value=f"{signal.get('confidence', 0)}%",
    )

with signal_4:
    st.metric(
        label="Signal Grade",
        value=safe_text(
            signal.get("grade", "-")
        ),
    )


# ==================================================
# ANALYSIS ACTIVITY
# ==================================================

render_html(
    """
    <div class="nexus-section-title" style="margin-top: 26px;">
        🛰️ Analysis Activity
    </div>
    """,
    unsafe_allow_html=True,
)

activity_items = [
    (
        "Market feed processed",
        f"{market.get('symbol', 'XAUUSD')} price "
        f"{price_text(market.get('price'))}",
        "#57D7FF",
    ),
    (
        "Trend engine completed",
        str(
            first_value(
                trend,
                "trend",
                "direction",
                fallback="Neutral",
            )
        ),
        state_colour(
            first_value(
                trend,
                "trend",
                "direction",
                fallback="Neutral",
            )
        ),
    ),
    (
        "Structure engine completed",
        str(
            first_value(
                structure,
                "structure",
                "direction",
                fallback="Neutral",
            )
        ),
        state_colour(
            first_value(
                structure,
                "structure",
                "direction",
                fallback="Neutral",
            )
        ),
    ),
    (
        "Liquidity scan completed",
        str(
            liquidity.get(
                "nearest_type",
                "None",
            )
        ),
        state_colour(
            liquidity.get(
                "nearest_type",
                "None",
            )
        ),
    ),
    (
        "Multi-timeframe scan completed",
        str(
            mtf.get(
                "direction",
                "Mixed",
            )
        ),
        state_colour(
            mtf.get(
                "direction",
                "Mixed",
            )
        ),
    ),
    (
        "AI decision generated",
        f"{decision} — {ai.get('confidence', 0)}%",
        decision_hex,
    ),
]

activity_html = ""

for title, detail, colour in activity_items:

    activity_html += f"""
    <div style="
        display: grid;
        grid-template-columns: 18px minmax(0, 1fr) auto;
        align-items: center;
        gap: 12px;
        padding: 13px 0;
        border-bottom: 1px solid rgba(87,215,255,0.10);
    ">
        <span style="
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: {colour};
            box-shadow: 0 0 13px {colour};
        "></span>

        <span style="
            color: #dceaff;
            font-size: 14px;
            font-weight: 700;
        ">
            {safe_text(title)}
        </span>

        <span style="
            color: {colour};
            font-size: 13px;
            font-weight: 700;
            text-align: right;
        ">
            {safe_text(detail)}
        </span>
    </div>
    """

render_html(
    f"""
    <div class="nexus-panel">
        {activity_html}
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# RISK NOTICE
# ==================================================

render_html(
    """
    <div style="
        position: relative;
        z-index: 2;
        margin-top: 26px;
        padding: 18px 20px;
        color: #d9c99b;
        font-size: 13px;
        line-height: 1.65;
        border: 1px solid rgba(255, 209, 102, 0.26);
        border-radius: 18px;
        background: rgba(255, 209, 102, 0.06);
        box-shadow: 0 14px 35px rgba(0,0,0,0.20);
    ">
        <strong style="color: #FFD166;">
            ⚠️ Risk Notice
        </strong>

        <br>

        ODI FX AI NEXUS is currently using simulated market data and
        experimental analysis logic. It does not guarantee profitable
        trades or a specific win rate. Verify every setup independently
        and never risk money you cannot afford to lose.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# FOOTER
# ==================================================

render_html(
    f"""
    <div style="
        position: relative;
        z-index: 2;
        margin-top: 28px;
        padding: 20px;
        color: #7189a8;
        font-size: 12px;
        text-align: center;
        letter-spacing: 0.08em;
        border-top: 1px solid rgba(87,215,255,0.12);
    ">
        {safe_text(APP_NAME)}
        &nbsp;•&nbsp;
        VERSION {safe_text(VERSION)}
        &nbsp;•&nbsp;
        XAUUSD INTELLIGENCE TERMINAL
    </div>
    """,
    unsafe_allow_html=True,
)