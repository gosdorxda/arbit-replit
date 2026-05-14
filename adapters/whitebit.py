import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class WhiteBitAdapter(BaseAdapter):
    BASE_URL = "https://whitebit.com/api/v1/public"

    @property
    def exchange_name(self) -> str:
        return "WHITEBIT"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/tickers",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            result = data.get('result', {})
            tickers = []

            for market, info in result.items():
                if not market.endswith('_USDT'):
                    continue

                base = market.replace('_USDT', '')
                ticker = info.get('ticker', {})

                price = self._safe_float(ticker.get('last'))
                volume_24h = self._safe_float(ticker.get('vol'))
                high_24h = self._safe_float(ticker.get('high'))
                low_24h = self._safe_float(ticker.get('low'))
                change_24h = self._safe_float(ticker.get('change', 0))
                turnover_24h = self._safe_float(ticker.get('deal', 0))

                if not price or price <= 0:
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
                    turnover_24h=turnover_24h
                )
                tickers.append(normalized)

            logger.info(f"WhiteBit: Fetched {len(tickers)} USDT pairs")
            return tickers

        except requests.RequestException as e:
            logger.error(f"WhiteBit API error: {str(e)}")
            raise Exception(f"Failed to fetch WhiteBit data: {str(e)}")

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            market = f"{base}_USDT"

            response = requests.get(
                f"{self.BASE_URL}/depth/result",
                params={"market": market, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            asks = []
            for entry in data.get('asks', []):
                price = self._safe_float(entry[0])
                amount = self._safe_float(entry[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})

            bids = []
            for entry in data.get('bids', []):
                price = self._safe_float(entry[0])
                amount = self._safe_float(entry[1])
                if price and amount:
                    bids.append({'price': price, 'amount': amount})

            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )

        except requests.RequestException as e:
            logger.error(f"WhiteBit orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch WhiteBit orderbook: {str(e)}")
