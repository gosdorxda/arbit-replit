import requests
import logging
from typing import List, Optional
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BiconomyAdapter(BaseAdapter):
    BASE_URL = "https://api.biconomy.com"
    HEADERS = {
        "X-SITE-ID": "127",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    @property
    def exchange_name(self) -> str:
        return "BICONOMY"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        url = f"{self.BASE_URL}/api/v1/tickers"
        
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Biconomy tickers: {e}")
            return []

        tickers = []
        ticker_list = data.get("ticker", [])
        
        for item in ticker_list:
            symbol = item.get("symbol", "")
            if not symbol.endswith("_USDT"):
                continue

            base = symbol.replace("_USDT", "")
            normalized_symbol = f"{base}/USDT"

            try:
                ticker = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=normalized_symbol,
                    base_currency=base,
                    quote_currency="USDT",
                    price=self._safe_float(item.get("last")),
                    volume_24h=self._safe_float(item.get("vol")),
                    high_24h=self._safe_float(item.get("high")),
                    low_24h=self._safe_float(item.get("low")),
                    change_24h=self._calculate_change(item),
                    turnover_24h=None
                )
                tickers.append(ticker)
            except Exception as e:
                logger.warning(f"Failed to parse Biconomy ticker {symbol}: {e}")
                continue

        logger.info(f"Fetched {len(tickers)} USDT pairs from Biconomy")
        return tickers

    def fetch_orderbook(self, symbol: str, limit: int = 10) -> Optional[NormalizedOrderbook]:
        api_symbol = symbol.replace("/", "_")
        limit = min(limit, 100)
        
        url = f"{self.BASE_URL}/api/v1/depth"
        params = {"symbol": api_symbol, "size": str(limit)}

        try:
            response = requests.get(url, params=params, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Biconomy orderbook for {symbol}: {e}")
            return None

        asks = []
        bids = []

        for ask in data.get("asks", [])[:limit]:
            if len(ask) >= 2:
                asks.append([self._safe_float(ask[0]), self._safe_float(ask[1])])

        for bid in data.get("bids", [])[:limit]:
            if len(bid) >= 2:
                bids.append([self._safe_float(bid[0]), self._safe_float(bid[1])])

        return NormalizedOrderbook(
            exchange=self.exchange_name,
            symbol=symbol,
            asks=asks,
            bids=bids,
            timestamp=None
        )

    def _calculate_change(self, item) -> Optional[float]:
        last = self._safe_float(item.get("last"))
        low = self._safe_float(item.get("low"))
        high = self._safe_float(item.get("high"))
        
        if last is None or low is None or high is None:
            return None
        if low == 0:
            return None
            
        mid = (high + low) / 2
        if mid == 0:
            return None
        return ((last - mid) / mid) * 100

    def _safe_float(self, value) -> Optional[float]:
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
