import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class VindaxAdapter(BaseAdapter):
    BASE_URL = "https://api.vindax.com/api/v1"
    
    @property
    def exchange_name(self) -> str:
        return "VINDAX"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/ticker/24hr",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                if not symbol.endswith('USDT'):
                    continue
                
                base = symbol.replace('USDT', '')
                
                price = self._safe_float(item.get('lastPrice'))
                volume_24h = self._safe_float(item.get('volume'))
                high_24h = self._safe_float(item.get('highPrice'))
                low_24h = self._safe_float(item.get('lowPrice'))
                turnover_24h = self._safe_float(item.get('quoteVolume'))
                
                open_price = self._safe_float(item.get('openPrice'))
                change_24h = self._safe_float(item.get('priceChangePercent'))
                if (change_24h is None or change_24h == 0) and price and open_price and open_price > 0:
                    change_24h = ((price - open_price) / open_price) * 100
                
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
            
            logger.info(f"Vindax: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Vindax API error: {str(e)}")
            raise Exception(f"Failed to fetch Vindax data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_symbol = symbol.replace('/', '')
            
            response = requests.get(
                f"{self.BASE_URL}/depth",
                params={
                    "symbol": api_symbol,
                    "limit": limit
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            asks = []
            for ask in data.get('asks', []):
                price = self._safe_float(ask[0])
                amount = self._safe_float(ask[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in data.get('bids', []):
                price = self._safe_float(bid[0])
                amount = self._safe_float(bid[1])
                if price and amount:
                    bids.append({'price': price, 'amount': amount})
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"Vindax orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Vindax orderbook: {str(e)}")
