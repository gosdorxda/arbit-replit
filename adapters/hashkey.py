import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker

logger = logging.getLogger(__name__)


class HashKeyAdapter(BaseAdapter):
    BASE_URL = "https://api-glb.hashkey.com"
    
    @property
    def exchange_name(self) -> str:
        return "HASHKEY"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/quote/v1/ticker/24hr",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                symbol = item.get('s', item.get('symbol', ''))
                
                if not symbol.endswith('USDT'):
                    continue
                
                base_currency = symbol.replace('USDT', '')
                
                open_price = self._safe_float(item.get('o', item.get('openPrice', 0)))
                close_price = self._safe_float(item.get('c', item.get('lastPrice', 0)))
                
                if open_price > 0:
                    change_pct = ((close_price - open_price) / open_price) * 100
                else:
                    change_pct = self._safe_float(item.get('p', item.get('priceChangePercent', 0)))
                
                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base_currency}/USDT",
                    base_currency=base_currency,
                    quote_currency='USDT',
                    price=close_price,
                    volume_24h=self._safe_float(item.get('v', item.get('volume', 0))),
                    high_24h=self._safe_float(item.get('h', item.get('highPrice', 0))),
                    low_24h=self._safe_float(item.get('l', item.get('lowPrice', 0))),
                    change_24h=change_pct,
                    turnover_24h=self._safe_float(item.get('qv', item.get('quoteVolume', 0)))
                )
                tickers.append(normalized)
            
            logger.info(f"HASHKEY: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"HASHKEY API error: {str(e)}")
            raise Exception(f"Failed to fetch HashKey data: {str(e)}")
        except Exception as e:
            logger.error(f"HASHKEY processing error: {str(e)}")
            raise
