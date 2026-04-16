import requests
import logging
from typing import List, Dict
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)

BASE_RENAME = {
    'XBT': 'BTC',
    'XDG': 'DOGE',
    'XET': 'ETH',
    'XXBT': 'BTC',
    'XETH': 'ETH',
    'XXRP': 'XRP',
    'XLTC': 'LTC',
    'XXLM': 'XLM',
    'XZEC': 'ZEC',
    'XXMR': 'XMR',
}

DISPLAY_TO_KRAKEN = {
    'BTC': 'XBT',
    'DOGE': 'XDG',
    'ETH': 'ETH',
    'XRP': 'XRP',
    'LTC': 'LTC',
    'XLM': 'XLM',
    'ZEC': 'ZEC',
    'XMR': 'XMR',
}

BATCH_SIZE = 100


class KrakenAdapter(BaseAdapter):
    BASE_URL = "https://api.kraken.com/0/public"

    @property
    def exchange_name(self) -> str:
        return "KRAKEN"

    def _get_all_pairs(self) -> Dict[str, dict]:
        response = requests.get(f"{self.BASE_URL}/AssetPairs", timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            raise Exception(f"Kraken AssetPairs error: {data['error']}")

        usdt_bases = set()
        usdt_pairs = {}
        usd_pairs = {}

        for pair_key, info in data.get('result', {}).items():
            quote = info.get('quote', '')
            raw_base = info.get('base', '')
            base = BASE_RENAME.get(raw_base, raw_base)
            wsname = info.get('wsname', '')

            if quote == 'USDT':
                usdt_bases.add(base)
                usdt_pairs[pair_key] = {'base': base, 'wsname': wsname, 'quote_type': 'USDT'}
            elif quote in ('ZUSD', 'USD'):
                usd_pairs[pair_key] = {'base': base, 'wsname': wsname, 'quote_type': 'USD'}

        combined = dict(usdt_pairs)
        for pair_key, info in usd_pairs.items():
            if info['base'] not in usdt_bases:
                combined[pair_key] = info

        return combined

    def _fetch_tickers_batch(self, pair_keys: List[str]) -> dict:
        results = {}
        for i in range(0, len(pair_keys), BATCH_SIZE):
            batch = pair_keys[i:i + BATCH_SIZE]
            response = requests.get(
                f"{self.BASE_URL}/Ticker",
                params={'pair': ','.join(batch)},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if data.get('error'):
                logger.warning(f"KRAKEN batch ticker error: {data['error']}")
                continue
            results.update(data.get('result', {}))
        return results

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            pairs = self._get_all_pairs()
            if not pairs:
                return []

            tick_data = self._fetch_tickers_batch(list(pairs.keys()))

            tickers = []
            for pair_key, tick in tick_data.items():
                info = pairs.get(pair_key)
                if not info:
                    continue

                base = info['base']
                price = self._safe_float(tick['c'][0])
                if price <= 0:
                    continue

                volume_24h = self._safe_float(tick['v'][1])
                high_24h = self._safe_float(tick['h'][1])
                low_24h = self._safe_float(tick['l'][1])
                open_price = self._safe_float(tick.get('o', 0))
                change_24h = ((price - open_price) / open_price) * 100 if open_price else 0.0
                turnover_24h = price * volume_24h if volume_24h else 0.0

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

            logger.info(f"KRAKEN: Fetched {len(tickers)} USDT+USD pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"KRAKEN API error: {str(e)}")
            raise Exception(f"Failed to fetch KRAKEN data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            kraken_base = DISPLAY_TO_KRAKEN.get(base, base)

            data = None
            for quote in ('USDT', 'USD'):
                pair_key = f"{kraken_base}{quote}"
                response = requests.get(
                    f"{self.BASE_URL}/Depth",
                    params={'pair': pair_key, 'count': limit},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                if not (data.get('error') and data['error']):
                    break

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
