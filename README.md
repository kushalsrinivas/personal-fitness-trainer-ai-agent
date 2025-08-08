# Crazybot — Stock Market Summary Bot (Google ADK + yfinance)

A minimal AI agent built with Google ADK that summarizes stocks and market indices using yfinance, with a custom DuckDuckGo web search tool and an optional FastAPI server exposing CORS-enabled endpoints.

## Features

- Stock snapshot: price, day change, recent-period return, 52w range, market cap, volumes
- Market overview: S&P 500, Nasdaq, Dow (configurable)
- Company headlines: recent news for a ticker
- Web search: DuckDuckGo-powered `web_search` for supporting links/context
- CORS-enabled API via `server.py`

## Requirements

- Python 3.10+
- ADK installed (verify: `adk --version`). If missing, follow ADK docs to install the CLI and Python package.
- Gemini API key for model access (Gemini Developer API):
  - `export GOOGLE_API_KEY="..."`

## Install

```bash
python -m venv venv
source venv/bin/activate
pip install -U yfinance pandas duckduckgo-search google-genai
# ADK should already be installed; if not, install per ADK docs
```

## Run (CORS-enabled FastAPI)

```bash
# Optional: allow your frontend origins (comma-separated)
export ALLOWED_ORIGINS="http://localhost:3000,https://yourapp.com"
# Optional: serve ADK web UI
export ADK_SERVE_WEB=true
# Optional: port/host
export PORT=8080
export HOST=0.0.0.0

python server.py
```

You should see the server listening on `http://localhost:8080`.

## Discover the app name

```bash
curl -s http://localhost:8080/list-apps
```

Expected to include `agent` as the app name (derived from the `agent/` folder).

## Create a session

```bash
curl -s -X POST \
  http://localhost:8080/apps/agent/users/demo/sessions/s1 \
  -H 'Content-Type: application/json' \
  -d '{"state":{}}'
```

## Ask the agent (non-streaming)

```bash
curl -s -X POST http://localhost:8080/run_sse \
  -H 'Content-Type: application/json' \
  -d '{
    "app_name": "agent",
    "user_id": "demo",
    "session_id": "s1",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Summarize AAPL today and for 1mo."}]
    },
    "streaming": false
  }'
```

## Tools available

- `get_stock_summary(ticker, period="1mo", interval="1d")`
- `get_market_overview(indexes="^GSPC,^IXIC,^DJI")`
- `get_company_news(ticker, limit=5)`
- `web_search(query, max_results=5, region="wt-wt", safesearch="moderate", timelimit="")`

Notes:

- Use empty string for `timelimit` if no limit (or `d|w|m|y`).
- The agent model is `gemini-2.0-flash` (set `GOOGLE_API_KEY`).

## Alternate: ADK built-in API server (no custom CORS)

```bash
adk api_server
```

For strict CORS control, prefer `python server.py` which sets `allow_origins`.

## Project layout

```
agent/
  __init__.py
  agent.py        # tools + root_agent
server.py          # FastAPI app with CORS via get_fast_api_app
venv/              # local virtual env (optional)
```

## Troubleshooting

- Automatic function calling prefers simple parameter types; this repo keeps tool signatures simple (no unions).
- If CORS fails, confirm `ALLOWED_ORIGINS` and that you’re running `server.py` (not plain `adk api_server`).
- Ensure `GOOGLE_API_KEY` is set and valid for Gemini.
