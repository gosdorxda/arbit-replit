import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)

BASE_RENAME = {
    'XBT': 'BTC',
    'XDG': 'DOGE',
}


class KrakenAdapter(BaseAdapter):
    BASE_URL = "https://api.kraken.com/0/public"

    @property
    def exchange_name(self) -> str:
        return "KRAKEN"

    def _get_usdt_pairs(self):
        response = requests.get(f"{self.BASE_URL}/AssetPairs", timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            raise Exception(f"Kraken AssetPairs error: {data['error']}")

        pairs = {}
        for pair_key, info in data.get('result', {}).items():
            if info.get('quote') != 'USDT':
                continue
            base = info.get('base', '')
            base = BASE_RENAME.get(base, base)
            wsname = info.get('wsname', '')
            pairs[pair_key] = {
                'base': base,
                'wsname': wsname,
            }
        return pairs

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            pairs = self._get_usdt_pairs()
            if not pairs:
                return []

            pair_str = ','.join(pairs.keys())
            response = requests.get(
                f"{self.BASE_URL}/Ticker",
                params={'pair': pair_str},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if data.get('error'):
                raise Exception(f"Kraken Ticker error: {data['error']}")

            tickers = []
            for pair_key, tick in data.get('result', {}).items():
                info = pairs.get(pair_key)
                if not info:
                    continue

                base = info['base']
                price = self._safe_float(tick['c'][0])
                volume_24h = self._safe_float(tick['v'][1])
                high_24h = self._safe_float(tick['h'][1])
                low_24h = self._safe_float(tick['l'][1])
                open_price = self._safe_float(tick.get('o', 0))
                if open_price and price:
                    change_24h = ((price - open_price) / open_price) * 100
                else:
                    change_24h = 0.0
                turnover_24h = price * volume_24h if price and volume_24h else 0.0

                if price <= 0:
                    continue

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
                    turnover_24h=turnover_24h,
                )
                tickers.append(normalized)

            logger.info(f"KRAKEN: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"KRAKEN API error: {str(e)}")
            raise Exception(f"Failed to fetch KRAKEN data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            kraken_base = {v: k for k, v in BASE_RENAME.items()}.get(base, base)
            pair_key = f"{kraken_base}USDT"

            response = requests.get(
                f"{self.BASE_URL}/Depth",
                params={'pair': pair_key, 'count': limit},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if data.get('error'):
                raise Exception(f"Kraken Depth error: {data['error']}")

            result = data.get('result', {})
            book = list(result.values())[0] if result else {}

            asks = []
            for row in book.get('asks', [])[:limit]:
                price = self._safe_float(row[0])
                amount = self._safe_float(row[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})

            bids = []
            for row in book.get('bids', [])[:limit]:
                price = self._safe_float(row[0])
                amount = self._safe_float(row[1])
                if price and amount:
                    bids.append({'price': price, 'amount': amount})

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
            )

        except requests.RequestException as e:
            logger.error(f"KRAKEN orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch KRAKEN orderbook: {str(e)}")
