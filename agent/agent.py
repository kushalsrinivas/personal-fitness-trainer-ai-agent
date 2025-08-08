from typing import Any, Dict, List
import pandas as pd
from google.adk.agents import Agent

# External deps for market data
import yfinance as yf
from duckduckgo_search import DDGS


def _pct(a: float | None, b: float | None) -> float | None:
    if a is None or b in (None, 0):
        return None
    return (a - b) / b * 100.0


def get_stock_summary(ticker: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
    """Fetch a concise snapshot of a stock using Yahoo Finance.

    Args:
        ticker: Symbol, e.g. "AAPL".
        period: Lookback window for history, e.g. "1mo", "3mo", "1y".
        interval: Candle interval, e.g. "1d", "1h".

    Returns:
        dict with status and a payload containing key metrics.
    """
    try:
        t = yf.Ticker(ticker)
        # Minimal recent history for day change
        hist = t.history(period="5d", interval="1d")
        if hist.empty:
            return {"status": "error", "error_message": f"No data for '{ticker}'."}

        last_close = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else None
        day_change_pct = _pct(last_close, prev_close)

        # Broader context
        ctx = t.history(period=period, interval=interval)
        perf_pct = None
        if len(ctx) > 1:
            perf_pct = _pct(float(ctx["Close"].iloc[-1]), float(ctx["Close"].iloc[0]))

        # Fast info when available
        fi = getattr(t, "fast_info", None)
        market_cap = getattr(fi, "market_cap", None)
        year_low = getattr(fi, "year_low", None)
        year_high = getattr(fi, "year_high", None)
        currency = getattr(fi, "currency", None)
        ten_day_avg_vol = getattr(fi, "ten_day_average_volume", None)
        three_month_avg_vol = getattr(fi, "three_month_average_volume", None)

        # Fallback 52w if fast_info missing
        if year_low is None or year_high is None:
            last_year = t.history(period="1y", interval="1d")
            if not last_year.empty:
                year_low = float(last_year["Low"].min())
                year_high = float(last_year["High"].max())

        payload: Dict[str, Any] = {
            "ticker": ticker.upper(),
            "price": last_close,
            "prev_close": prev_close,
            "day_change_pct": day_change_pct,
            "period": period,
            "interval": interval,
            "period_return_pct": perf_pct,
            "52w_low": year_low,
            "52w_high": year_high,
            "market_cap": market_cap,
            "currency": currency,
            "volume": int(hist["Volume"].iloc[-1]) if "Volume" in hist.columns else None,
            "avg_volume_10d": ten_day_avg_vol,
            "avg_volume_3m": three_month_avg_vol,
        }
        return {"status": "success", "data": payload}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error_message": f"Failed to fetch {ticker}: {e}"}


def get_market_overview(indexes: str = "^GSPC,^IXIC,^DJI") -> Dict[str, Any]:
    """Return snapshot for key indexes (default: S&P 500, Nasdaq, Dow)."""
    try:
        symbols = indexes.split(",")
        data = yf.download(symbols, period="5d", interval="1d", group_by="ticker", progress=False)
        results: Dict[str, Any] = {}
        for sym in symbols:
            try:
                df = data[sym] if isinstance(data.columns, pd.MultiIndex) else data
            except Exception:  # noqa: BLE001
                df = data
            if df.empty:
                results[sym] = {"status": "error", "error_message": "No data"}
                continue
            last_close = float(df["Close"].iloc[-1])
            prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else None
            results[sym] = {
                "status": "success",
                "price": last_close,
                "prev_close": prev_close,
                "day_change_pct": _pct(last_close, prev_close),
            }
        return {"status": "success", "data": results}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error_message": f"Failed market overview: {e}"}


def get_company_news(ticker: str, limit: int = 5) -> Dict[str, Any]:
    """Return the latest company-related headlines via Yahoo Finance."""
    try:
        t = yf.Ticker(ticker)
        items = t.news or []
        trimmed = [
            {
                "title": i.get("title"),
                "link": i.get("link"),
                "publisher": i.get("publisher"),
                "published": i.get("providerPublishTime"),
            }
            for i in items[: max(0, int(limit))]
        ]
        return {"status": "success", "data": {"ticker": ticker.upper(), "news": trimmed}}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error_message": f"Failed news for {ticker}: {e}"}


def web_search(query: str, max_results: int = 5, region: str = "wt-wt", safesearch: str = "moderate", timelimit: str = "") -> Dict[str, Any]:
    """Lightweight web search via DuckDuckGo.

    Args:
        query: Search query.
        max_results: Number of results to return.
        region: Region code, e.g., 'wt-wt' (worldwide).
        safesearch: 'off' | 'moderate' | 'strict'.
        timelimit: 'd','w','m','y' to limit by time. Use empty string for no limit.

    Returns:
        dict with status and list of results [{title, href, snippet, source}].
    """
    try:
        results: List[Dict[str, Any]] = []
        with DDGS() as ddgs:
            tl = None if not timelimit else timelimit
            for r in ddgs.text(query, region=region, safesearch=safesearch, timelimit=tl, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "snippet": r.get("body"),
                    "source": r.get("source"),
                })
        return {"status": "success", "data": results}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error_message": f"Search failed: {e}"}


root_agent = Agent(
    name="stock_market_bot",
    model="gemini-2.0-flash",
    description="Summarizes stocks and market using yfinance and tools.",
    instruction=
    """
    You are a stock market assistant.
    - For overall market or indexes, call get_market_overview.
    - For a specific ticker snapshot, call get_stock_summary.
    - For latest headlines for a ticker, call get_company_news.
    - If you need web context or supporting links, call web_search.
    After calling tools, produce a concise summary with key numbers and changes.
    Do not provide investment advice. Clearly label figures with currency when provided.
    """,
    tools=[web_search, get_stock_summary, get_market_overview, get_company_news],
)