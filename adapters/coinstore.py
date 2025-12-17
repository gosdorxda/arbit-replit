import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class CoinstoreAdapter(BaseAdapter):
    BASE_URL = "https://api.coinstore.com/api/v1/market"
    
    @property
    def exchange_name(self) -> str:
        return "COINSTORE"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/tickers",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            data = result.get('data', [])
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                if not symbol.endswith('USDT'):
                    continue
                
                base = symbol.replace('USDT', '')
                
                price = self._safe_float(item.get('close'))
                volume_24h = self._safe_float(item.get('volume'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                turnover_24h = self._safe_float(item.get('amount'))
                
                open_price = self._safe_float(item.get('open'))
                change_24h = None
                if price and open_price and open_price > 0:
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
            
            logger.info(f"Coinstore: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Coinstore API error: {str(e)}")
            raise Exception(f"Failed to fetch Coinstore data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_symbol = symbol.replace('/', '')
            
            response = requests.get(
                f"{self.BASE_URL}/depth/{api_symbol}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            data = result.get('data', {})
            
            asks = []
            for ask in data.get('a', []):
                price = self._safe_float(ask[0])
                amount = self._safe_float(ask[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in data.get('b', []):
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
            logger.error(f"Coinstore orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Coinstore orderbook: {str(e)}")
