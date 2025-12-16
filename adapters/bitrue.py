import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BitrueAdapter(BaseAdapter):
    BASE_URL = "https://openapi.bitrue.com"
    
    @property
    def exchange_name(self) -> str:
        return "BITRUE"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/api/v1/ticker/24hr",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                
                if not symbol.endswith('USDT'):
                    continue
                
                base_currency = symbol.replace('USDT', '')
                
                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base_currency}/USDT",
                    base_currency=base_currency,
                    quote_currency='USDT',
                    price=self._safe_float(item.get('lastPrice')),
                    volume_24h=self._safe_float(item.get('volume')),
                    high_24h=self._safe_float(item.get('highPrice')),
                    low_24h=self._safe_float(item.get('lowPrice')),
                    change_24h=self._safe_float(item.get('priceChangePercent')),
                    turnover_24h=self._safe_float(item.get('quoteVolume'))
                )
                tickers.append(normalized)
            
            logger.info(f"BITRUE: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"BITRUE API error: {str(e)}")
            raise Exception(f"Failed to fetch BITRUE data: {str(e)}")
        except Exception as e:
            logger.error(f"BITRUE processing error: {str(e)}")
            raise
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_symbol = symbol.replace('/', '')
            
            response = requests.get(
                f"https://www.bitrue.com/api/v1/depth",
                params={"symbol": api_symbol, "limit": min(limit, 100)},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            asks = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in data.get('asks', [])]
            bids = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in data.get('bids', [])]
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
                timestamp=data.get('lastUpdateId')
            )
            
        except requests.RequestException as e:
            logger.error(f"BITRUE orderbook API error: {str(e)}")
            raise Exception(f"Failed to fetch BITRUE orderbook: {str(e)}")
        except Exception as e:
            logger.error(f"BITRUE orderbook processing error: {str(e)}")
            raise
