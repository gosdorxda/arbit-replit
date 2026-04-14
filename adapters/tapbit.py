import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class TapbitAdapter(BaseAdapter):
    BASE_URL = "https://openapi.tapbit.com"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.tapbit.com",
        "Referer": "https://www.tapbit.com/",
    }

    @property
    def exchange_name(self) -> str:
        return "TAPBIT"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/spot/api/v1/ticker/24hr",
                headers=self.HEADERS,
                timeout=30,
            )
            if response.status_code == 403:
                raise Exception(
                    "Tapbit API returned 403 Forbidden — the API may be geo-restricted "
                    "or blocking requests from cloud/server IPs. Try again later or from a different network."
                )
            response.raise_for_status()
            data = response.json()

            items = data if isinstance(data, list) else data.get("data", [])

            tickers = []
            for item in items:
                instrument_id = item.get("instrumentId", "")
                if not instrument_id.endswith("_USDT"):
                    continue

                base = instrument_id.replace("_USDT", "")
                price = self._safe_float(item.get("last"))
                volume_24h = self._safe_float(item.get("volume24h", 0))
                high_24h = self._safe_float(item.get("high24h", 0))
                low_24h = self._safe_float(item.get("low24h", 0))
                change_pct = item.get("chgRate", item.get("changeRate", "0"))
                change_24h = self._safe_float(str(change_pct).replace("%", ""))
                if abs(change_24h) > 1:
                    change_24h = change_24h
                else:
                    change_24h = change_24h * 100
                turnover_24h = self._safe_float(item.get("turnover24h", item.get("quoteVolume24h", 0)))
                if not turnover_24h and price and volume_24h:
                    turnover_24h = price * volume_24h

                if price <= 0:
                    continue

                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base}/USDT",
                    base_currency=base,
                    quote_currency="USDT",
                    price=price,
                    volume_24h=volume_24h,
                    high_24h=high_24h,
                    low_24h=low_24h,
                    change_24h=change_24h,
                    turnover_24h=turnover_24h,
                )
                tickers.append(normalized)

            logger.info(f"TAPBIT: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"TAPBIT API error: {str(e)}")
            raise Exception(f"Failed to fetch TAPBIT data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace("/USDT", "")
            instrument_id = f"{base}_USDT"

            response = requests.get(
                f"{self.BASE_URL}/spot/api/v1/depth",
                headers=self.HEADERS,
                params={"instrumentId": instrument_id, "depth": limit},
                timeout=10,
            )
            if response.status_code == 403:
                raise Exception("Tapbit API is blocked from this network (403 Forbidden).")
            response.raise_for_status()
            data = response.json()

            book = data if isinstance(data, dict) and "asks" in data else data.get("data", {})

            asks = []
            for row in book.get("asks", [])[:limit]:
                if isinstance(row, list) and len(row) >= 2:
                    price = self._safe_float(row[0])
                    amount = self._safe_float(row[1])
                elif isinstance(row, dict):
                    price = self._safe_float(row.get("price", 0))
                    amount = self._safe_float(row.get("qty", row.get("amount", 0)))
                else:
                    continue
                if price and amount:
                    asks.append({"price": price, "amount": amount})

            bids = []
            for row in book.get("bids", [])[:limit]:
                if isinstance(row, list) and len(row) >= 2:
                    price = self._safe_float(row[0])
                    amount = self._safe_float(row[1])
                elif isinstance(row, dict):
                    price = self._safe_float(row.get("price", 0))
                    amount = self._safe_float(row.get("qty", row.get("amount", 0)))
                else:
                    continue
                if price and amount:
                    bids.append({"price": price, "amount": amount})

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
            )

        except requests.RequestException as e:
            logger.error(f"TAPBIT orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch TAPBIT orderbook: {str(e)}")
