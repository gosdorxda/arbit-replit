import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class HTXAdapter(BaseAdapter):
    # Using api.huobi.pro (old Huobi domain) because api.htx.com is
    # Cloudflare-blocked in many server environments. Both domains serve
    # the same HTX exchange API.
    BASE_URL = "https://api.huobi.pro"

    @property
    def exchange_name(self) -> str:
        return "HTX"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/market/tickers",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'ok':
                raise Exception(f"HTX API returned status: {data.get('status')}")

            tickers = []
            for item in data.get('data', []):
                symbol = item.get('symbol', '')
                if not symbol.endswith('usdt'):
                    continue

                base = symbol[:-4].upper()
                price = self._safe_float(item.get('close'))
                open_price = self._safe_float(item.get('open'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                volume_24h = self._safe_float(item.get('amount'))
                turnover_24h = self._safe_float(item.get('vol'))

                if not price or price <= 0:
                    continue

                if open_price and open_price > 0:
                    change_24h = (price - open_price) / open_price * 100
                else:
                    change_24h = 0.0

                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base}/USDT",
                    base_currency=base,
                    quote_currency='USDT',
                    price=price,
                    volume_24h=volume_24h,
                    high_24h=high_24h,
                    low_24h=low_24h,
                    change_24h=change_24h,
                    turnover_24h=turnover_24h
                )
                tickers.append(normalized)

            logger.info(f"HTX: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"HTX API error: {str(e)}")
            raise Exception(f"Failed to fetch HTX data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').lower()
            htx_symbol = f"{base}usdt"

            response = requests.get(
                f"{self.BASE_URL}/market/depth",
                params={"symbol": htx_symbol, "type": "step0", "depth": limit},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            tick = data.get('tick', {})

            asks = []
            for entry in tick.get('asks', []):
                price = self._safe_float(entry[0])
                amount = self._safe_float(entry[1])
                if price and amount:
                    asks.append([price, amount])

            bids = []
            for entry in tick.get('bids', []):
                price = self._safe_float(entry[0])
                amount = self._safe_float(entry[1])
                if price and amount:
                    bids.append([price, amount])

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )

        except requests.RequestException as e:
            logger.error(f"HTX orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch HTX orderbook: {str(e)}")
