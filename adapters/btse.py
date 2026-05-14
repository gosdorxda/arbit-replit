import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BTSEAdapter(BaseAdapter):
    BASE_URL = "https://api.btse.com/spot/api/v3.2"

    @property
    def exchange_name(self) -> str:
        return "BTSE"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/market_summary",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                if not symbol.endswith('-USDT'):
                    continue

                base = symbol.replace('-USDT', '')

                price = self._safe_float(item.get('last'))
                volume_24h = self._safe_float(item.get('volume'))
                high_24h = self._safe_float(item.get('high24Hr'))
                low_24h = self._safe_float(item.get('low24Hr'))
                change_24h = self._safe_float(item.get('percentageChange'))

                turnover_24h = None
                if price and volume_24h:
                    turnover_24h = price * volume_24h

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

            logger.info(f"BTSE: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"BTSE API error: {str(e)}")
            raise Exception(f"Failed to fetch BTSE data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_symbol = symbol.replace('/', '-')

            response = requests.get(
                f"{self.BASE_URL}/orderbook/L2",
                params={'symbol': api_symbol, 'depth': limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            asks = []
            for entry in (data.get('sellQuote') or [])[:limit]:
                price = self._safe_float(entry.get('price'))
                amount = self._safe_float(entry.get('size'))
                if price and amount:
                    asks.append({'price': price, 'amount': amount})

            bids = []
            for entry in (data.get('buyQuote') or [])[:limit]:
                price = self._safe_float(entry.get('price'))
                amount = self._safe_float(entry.get('size'))
                if price and amount:
                    bids.append({'price': price, 'amount': amount})

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )

        except requests.RequestException as e:
            logger.error(f"BTSE orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch BTSE orderbook: {str(e)}")
