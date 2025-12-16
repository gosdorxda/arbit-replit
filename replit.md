# Crypto Exchange Data Aggregator

## Overview
A Flask-based web application that fetches, normalizes, and displays SPOT/USDT market data from multiple cryptocurrency exchanges. Currently supports LBANK and HashKey exchanges.

## Key Features
- **Manual Data Fetching**: Button-triggered fetching from each exchange
- **Data Normalization**: Adapter pattern to normalize different API response formats to a unified schema
- **Persistent Storage**: PostgreSQL database for storing normalized ticker data
- **Interactive Table**: Filtering, sorting, and searching capabilities
- **Status Tracking**: Fetch logs and status indicators for each exchange
- **Orderbook Viewing**: Modal popup showing real-time bid/ask depth for any trading pair

## Project Architecture

### Backend (Flask + Python)
```
app.py              - Flask app configuration and database setup
main.py             - Entry point
models.py           - SQLAlchemy models (SpotTicker, FetchLog)
routes.py           - Flask routes and API endpoints
adapters/
  ├── __init__.py   - Adapter exports
  ├── base.py       - BaseAdapter abstract class and NormalizedTicker dataclass
  ├── lbank.py      - LBANK exchange adapter
  └── hashkey.py    - HashKey exchange adapter
```

### Frontend
```
templates/
  └── index.html    - Main page template
static/
  ├── css/style.css - Styling
  └── js/main.js    - Frontend logic
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/api/fetch/lbank` | POST | Trigger LBANK data fetch |
| `/api/fetch/hashkey` | POST | Trigger HashKey data fetch |
| `/api/tickers` | GET | Get all stored ticker data |
| `/api/status` | GET | Get fetch status for each exchange |
| `/api/logs` | GET | Get recent fetch logs |
| `/api/orderbook/<exchange>/<symbol>` | GET | Get orderbook depth data (asks/bids) |

## Data Normalization

Each exchange adapter transforms exchange-specific API responses into a unified `NormalizedTicker` format:

| Field | Description |
|-------|-------------|
| exchange | Exchange name (LBANK, HASHKEY) |
| symbol | Trading pair (e.g., BTC/USDT) |
| base_currency | Base asset (e.g., BTC) |
| quote_currency | Quote asset (always USDT) |
| price | Current price |
| volume_24h | 24-hour trading volume |
| high_24h | 24-hour high price |
| low_24h | 24-hour low price |
| change_24h | 24-hour price change percentage |
| turnover_24h | 24-hour turnover value |

## Adding New Exchanges

To add a new exchange:

1. Create a new adapter file in `adapters/` (e.g., `binance.py`)
2. Extend `BaseAdapter` and implement `exchange_name` property and `fetch_usdt_tickers()` method
3. Export the adapter in `adapters/__init__.py`
4. Add route in `routes.py` for the new exchange
5. Add button in `templates/index.html`

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SESSION_SECRET` - Flask session secret key

## Recent Changes
- Added orderbook viewing feature with modal popup for each trading pair
- Initial implementation with LBANK and HashKey adapters
- PostgreSQL database integration
- Interactive table with filtering and sorting
- Real-time status indicators
