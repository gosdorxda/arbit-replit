import requests
import logging
import time
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BingXAdapter(BaseAdapter):
    BASE_URL = "https://open-api.bingx.com/openApi/spot/v1"

    @property
    def exchange_name(self) -> str:
        return "BINGX"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            ts = int(time.time() * 1000)
            response = requests.get(
                f"{self.BASE_URL}/ticker/24hr",
                params={'timestamp': ts},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if data.get('code') != 0:
                raise Exception(f"BingX API error: {data.get('msg')}")

            tickers = []
            for item in data.get('data', []):
                symbol_raw = item.get('symbol', '')
                if not symbol_raw.endswith('-USDT'):
                    continue

                base = symbol_raw.replace('-USDT', '')
                price = self._safe_float(item.get('lastPrice', 0))
                if price <= 0:
                    continue

                open_price = self._safe_float(item.get('openPrice', 0))
                change_pct_str = str(item.get('priceChangePercent', '0%')).replace('%', '')
                change_24h = self._safe_float(change_pct_str)

                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base}/USDT",
                    base_currency=base,
                    quote_currency='USDT',
                    price=price,
                    volume_24h=self._safe_float(item.get('volume', 0)),
                    high_24h=self._safe_float(item.get('highPrice', 0)),
                    low_24h=self._safe_float(item.get('lowPrice', 0)),
                    change_24h=change_24h,
                    turnover_24h=self._safe_float(item.get('quoteVolume', 0)),
                )
                tickers.append(normalized)

            logger.info(f"BINGX: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"BINGX API error: {str(e)}")
            raise Exception(f"Failed to fetch BINGX data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            bingx_symbol = f"{base}-USDT"

            response = requests.get(
                f"{self.BASE_URL}/market/depth",
                params={'symbol': bingx_symbol, 'depth': limit},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get('code') != 0:
                raise Exception(f"BingX orderbook error: {data.get('msg')}")

            book = data.get('data', {})

            bids = []
            for row in book.get('bids', [])[:limit]:
                price = self._safe_float(row[0])
                amount = self._safe_float(row[1])
                if price and amount:
                    bids.append({'price': price, 'amount': amount})

            asks = []
            for row in book.get('asks', [])[:limit]:
                price = self._safe_float(row[0])
                amount = self._safe_float(row[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
            )

        except requests.RequestException as e:
            logger.error(f"BINGX orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch BINGX orderbook: {str(e)}")
