"""
ODI FX AI NEXUS

Live-Only XAU/USD Market Data Gateway

Provider: Twelve Data

Important:
- Uses live provider data only.
- Contains no simulated market data.
- Contains no fallback market data.
- Provider failures stop the analysis.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from settings import (
    DEFAULT_SYMBOL,
    DEFAULT_TIMEFRAME,
    MAX_CANDLES,
)


# ==================================================
# TWELVE DATA CONFIGURATION
# ==================================================

BASE_URL = "https://api.twelvedata.com"

REQUEST_TIMEOUT = 20

TWELVE_DATA_API_KEY = (
    os.getenv(
        "TWELVE_DATA_API_KEY",
        "",
    )
    .strip()
    .strip('"')
    .strip("'")
)

TWELVE_DATA_SYMBOL = (
    os.getenv(
        "TWELVE_DATA_SYMBOL",
        "XAU/USD",
    )
    .strip()
    .upper()
)


# ==================================================
# TIMEFRAME MAPPING
# ==================================================

INTERVAL_MAP = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "M45": "45min",
    "H1": "1h",
    "H2": "2h",
    "H4": "4h",
    "H8": "8h",
    "D1": "1day",
    "W1": "1week",
    "MN1": "1month",
}


# ==================================================
# CONFIGURATION VALIDATION
# ==================================================

def validate_configuration():
    """Validate the live market-data configuration."""

    if not TWELVE_DATA_API_KEY:
        raise RuntimeError(
            "TWELVE_DATA_API_KEY is missing. "
            "Add your Twelve Data API key to the "
            "Codespaces environment before starting the app."
        )

    if not TWELVE_DATA_SYMBOL:
        raise RuntimeError(
            "TWELVE_DATA_SYMBOL is missing."
        )

    if TWELVE_DATA_SYMBOL != "XAU/USD":
        raise RuntimeError(
            "This application is configured for XAU/USD only. "
            f"Received symbol: {TWELVE_DATA_SYMBOL}"
        )


def get_provider_interval():
    """Convert the application timeframe into provider format."""

    timeframe = str(
        DEFAULT_TIMEFRAME
    ).strip().upper()

    interval = INTERVAL_MAP.get(timeframe)

    if interval is None:
        supported = ", ".join(
            INTERVAL_MAP.keys()
        )

        raise RuntimeError(
            f"Unsupported timeframe: {timeframe}. "
            f"Supported timeframes: {supported}"
        )

    return interval


# ==================================================
# VALUE CONVERSION
# ==================================================

def convert_price(value, field_name):
    """Convert a provider price into a validated float."""

    if value in (None, "", "null"):
        raise RuntimeError(
            f"Live candle is missing {field_name}."
        )

    try:
        price = float(value)

    except (TypeError, ValueError) as error:
        raise RuntimeError(
            f"Invalid {field_name} value received: {value}"
        ) from error

    if price <= 0:
        raise RuntimeError(
            f"Invalid non-positive {field_name}: {price}"
        )

    return round(price, 5)


def convert_volume(value):
    """
    Convert provider volume.

    Spot-metal feeds may not include centralised volume.
    Zero is returned when the provider does not supply it.
    """

    if value in (None, "", "null"):
        return 0

    try:
        volume = int(float(value))

    except (TypeError, ValueError):
        return 0

    return max(volume, 0)


# ==================================================
# TWELVE DATA REQUEST
# ==================================================

def request_twelve_data(endpoint, parameters):
    """Send an authenticated request to Twelve Data."""

    validate_configuration()

    query = urlencode(parameters)

    request_url = (
        f"{BASE_URL}/{endpoint}?{query}"
    )

    request = Request(
        url=request_url,
        method="GET",
        headers={
            "Authorization": (
                f"apikey {TWELVE_DATA_API_KEY}"
            ),
            "Accept": "application/json",
            "User-Agent": "ODI-FX-AI-NEXUS/1.0",
        },
    )

    try:
        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:

            response_text = (
                response
                .read()
                .decode("utf-8")
            )

    except HTTPError as error:
        response_body = (
            error
            .read()
            .decode(
                "utf-8",
                errors="replace",
            )
        )

        if error.code == 401:
            message = (
                "Twelve Data rejected the API key. "
                "Confirm TWELVE_DATA_API_KEY contains your "
                "complete personal API key."
            )

        elif error.code == 403:
            message = (
                "Your Twelve Data plan does not have permission "
                "to access the requested XAU/USD data."
            )

        elif error.code == 429:
            message = (
                "The Twelve Data API request limit was reached. "
                "Wait for the provider limit to reset."
            )

        else:
            message = (
                "Twelve Data rejected the live-data request."
            )

        raise RuntimeError(
            f"{message} "
            f"HTTP {error.code}: {response_body}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            "Unable to connect to Twelve Data. "
            f"Network error: {error.reason}"
        ) from error

    except TimeoutError as error:
        raise RuntimeError(
            "The Twelve Data live-data request timed out."
        ) from error

    try:
        payload = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Twelve Data returned invalid JSON."
        ) from error

    if not isinstance(payload, dict):
        raise RuntimeError(
            "Twelve Data returned an unexpected response."
        )

    if payload.get("status") == "error":
        error_code = payload.get(
            "code",
            "unknown",
        )

        error_message = payload.get(
            "message",
            "Unknown Twelve Data error.",
        )

        raise RuntimeError(
            "Twelve Data live-data request failed. "
            f"Code {error_code}: {error_message}"
        )

    return payload


# ==================================================
# CANDLE CONVERSION
# ==================================================

def convert_candle(provider_candle):
    """Convert one provider candle into application format."""

    if not isinstance(provider_candle, dict):
        raise RuntimeError(
            "Invalid live candle format received."
        )

    candle_time = provider_candle.get(
        "datetime"
    )

    if not candle_time:
        raise RuntimeError(
            "Live candle is missing its datetime."
        )

    open_price = convert_price(
        provider_candle.get("open"),
        "open",
    )

    high_price = convert_price(
        provider_candle.get("high"),
        "high",
    )

    low_price = convert_price(
        provider_candle.get("low"),
        "low",
    )

    close_price = convert_price(
        provider_candle.get("close"),
        "close",
    )

    if high_price < low_price:
        raise RuntimeError(
            "Provider candle high is below its low."
        )

    if high_price < max(
        open_price,
        close_price,
    ):
        raise RuntimeError(
            "Provider candle high is invalid."
        )

    if low_price > min(
        open_price,
        close_price,
    ):
        raise RuntimeError(
            "Provider candle low is invalid."
        )

    return {
        "time": str(candle_time),
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": convert_volume(
            provider_candle.get("volume")
        ),
    }


# ==================================================
# LIVE XAU/USD MARKET DATA
# ==================================================

def get_market_data(count=MAX_CANDLES):
    """
    Download and return live XAU/USD candles.

    There is no simulated or alternative fallback.
    Any provider failure stops the market analysis.
    """

    validate_configuration()

    try:
        requested_count = int(count)

    except (TypeError, ValueError) as error:
        raise RuntimeError(
            f"Invalid candle count: {count}"
        ) from error

    requested_count = max(
        50,
        min(requested_count, 5000),
    )

    interval = get_provider_interval()

    payload = request_twelve_data(
        endpoint="time_series",
        parameters={
            "symbol": TWELVE_DATA_SYMBOL,
            "interval": interval,
            "outputsize": requested_count,
            "format": "JSON",
            "order": "asc",
            "timezone": "UTC",
        },
    )

    provider_values = payload.get(
        "values"
    )

    if not isinstance(
        provider_values,
        list,
    ):
        raise RuntimeError(
            "Twelve Data did not return a candle list."
        )

    if not provider_values:
        raise RuntimeError(
            "Twelve Data returned no live XAU/USD candles."
        )

    candles = [
        convert_candle(provider_candle)
        for provider_candle in provider_values
    ]

    # Keep the candle list strictly oldest to newest.
    candles.sort(
        key=lambda candle: candle["time"]
    )

    latest = candles[-1]

    latest_price = latest["close"]
    latest_volume = latest["volume"]

    metadata = payload.get(
        "meta",
        {},
    )

    if not isinstance(metadata, dict):
        metadata = {}

    provider_symbol = metadata.get(
        "symbol",
        TWELVE_DATA_SYMBOL,
    )

    provider_interval = metadata.get(
        "interval",
        interval,
    )

    return {
        "symbol": DEFAULT_SYMBOL,
        "provider_symbol": provider_symbol,
        "timeframe": DEFAULT_TIMEFRAME,
        "provider_interval": provider_interval,

        "price": latest_price,

        # The time-series endpoint supplies OHLC candles.
        # It does not supply a broker-specific bid/ask spread.
        "bid": None,
        "ask": None,
        "spread": None,

        "volume": latest_volume,
        "volume_available": latest_volume > 0,

        "time": latest["time"],
        "candles": candles,

        "data_mode": "LIVE",
        "provider": "Twelve Data",
        "provider_type": metadata.get(
            "type",
            "Precious Metal",
        ),

        "currency_base": metadata.get(
            "currency_base",
            "Gold Spot",
        ),

        "currency_quote": metadata.get(
            "currency_quote",
            "US Dollar",
        ),

        "exchange_timezone": metadata.get(
            "exchange_timezone",
            "UTC",
        ),

        "spread_estimated": False,
        "provider_error": None,
    }