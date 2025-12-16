import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class PoloniexAdapter(BaseAdapter):
    BASE_URL = "https://api.poloniex.com"
    
    @property
    def exchange_name(self) -> str:
        return "POLONIEX"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/markets/ticker24h",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                if not symbol.endswith('_USDT'):
                    continue
                
                base = symbol.replace('_USDT', '')
                
                price = self._safe_float(item.get('close'))
                volume_24h = self._safe_float(item.get('quantity'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                change_pct = self._safe_float(item.get('dailyChange', 0))
                change_24h = change_pct * 100 if change_pct else 0
                turnover_24h = self._safe_float(item.get('amount', 0))
                
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
            
            logger.info(f"Poloniex: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Poloniex API error: {str(e)}")
            raise Exception(f"Failed to fetch Poloniex data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '')
            api_symbol = f"{base}_USDT"
            
            response = requests.get(
                f"{self.BASE_URL}/markets/{api_symbol}/orderBook",
                params={"limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            asks_raw = data.get('asks', [])
            asks = []
            for i in range(0, min(len(asks_raw), 20), 2):
                price = self._safe_float(asks_raw[i])
                amount = self._safe_float(asks_raw[i + 1]) if i + 1 < len(asks_raw) else 0
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids_raw = data.get('bids', [])
            bids = []
            for i in range(0, min(len(bids_raw), 20), 2):
                price = self._safe_float(bids_raw[i])
                amount = self._safe_float(bids_raw[i + 1]) if i + 1 < len(bids_raw) else 0
                if price and amount:
                    bids.append({'price': price, 'amount': amount})
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"Poloniex orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Poloniex orderbook: {str(e)}")
