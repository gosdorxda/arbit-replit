import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class AscendEXAdapter(BaseAdapter):
    BASE_URL = "https://ascendex.com"
    
    @property
    def exchange_name(self) -> str:
        return "ASCENDEX"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/api/pro/v1/spot/ticker",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 0:
                raise Exception(f"AscendEX API error: {result.get('message', 'Unknown error')}")
            
            data = result.get('data', [])
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                
                if not symbol.endswith('/USDT'):
                    continue
                
                base_currency = symbol.replace('/USDT', '')
                price = self._safe_float(item.get('close'))
                volume = self._safe_float(item.get('volume'))
                
                open_price = self._safe_float(item.get('open'))
                change_24h = 0.0
                if open_price and open_price > 0 and price:
                    change_24h = ((price - open_price) / open_price) * 100
                
                turnover = price * volume if price and volume else 0.0
                
                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    base_currency=base_currency,
                    quote_currency='USDT',
                    price=price,
                    volume_24h=volume,
                    high_24h=self._safe_float(item.get('high')),
                    low_24h=self._safe_float(item.get('low')),
                    change_24h=change_24h,
                    turnover_24h=turnover
                )
                tickers.append(normalized)
            
            logger.info(f"ASCENDEX: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"ASCENDEX API error: {str(e)}")
            raise Exception(f"Failed to fetch ASCENDEX data: {str(e)}")
        except Exception as e:
            logger.error(f"ASCENDEX processing error: {str(e)}")
            raise
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            response = requests.get(
                f"{self.BASE_URL}/api/pro/v2/depth",
                params={"symbol": symbol},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 0:
                raise Exception(f"AscendEX API error: {result.get('message', 'Unknown error')}")
            
            orderbook_data = result.get('data', {}).get('data', {})
            
            asks = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in orderbook_data.get('asks', [])[:limit]]
            bids = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in orderbook_data.get('bids', [])[:limit]]
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
                timestamp=orderbook_data.get('ts')
            )
            
        except requests.RequestException as e:
            logger.error(f"ASCENDEX orderbook API error: {str(e)}")
            raise Exception(f"Failed to fetch ASCENDEX orderbook: {str(e)}")
        except Exception as e:
            logger.error(f"ASCENDEX orderbook processing error: {str(e)}")
            raise
