import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BitMartAdapter(BaseAdapter):
    BASE_URL = "https://api-cloud.bitmart.com"
    
    @property
    def exchange_name(self) -> str:
        return "BITMART"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/spot/quotation/v3/tickers",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 1000:
                raise Exception(f"BitMart API error: {result.get('message')}")
            
            data = result.get('data', [])
            
            tickers = []
            for item in data:
                symbol = item[0]
                
                if not symbol.endswith('_USDT'):
                    continue
                
                base_currency = symbol.replace('_USDT', '')
                
                price = self._safe_float(item[1])
                volume_24h = self._safe_float(item[2])
                turnover_24h = self._safe_float(item[3])
                open_24h = self._safe_float(item[4])
                high_24h = self._safe_float(item[5])
                low_24h = self._safe_float(item[6])
                fluctuation = self._safe_float(item[7])
                
                change_24h = fluctuation * 100 if fluctuation else 0
                
                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base_currency}/USDT",
                    base_currency=base_currency,
                    quote_currency='USDT',
                    price=price,
                    volume_24h=volume_24h,
                    high_24h=high_24h,
                    low_24h=low_24h,
                    change_24h=change_24h,
                    turnover_24h=turnover_24h
                )
                tickers.append(normalized)
            
            logger.info(f"BitMart: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"BitMart API error: {str(e)}")
            raise Exception(f"Failed to fetch BitMart data: {str(e)}")
        except Exception as e:
            logger.error(f"BitMart processing error: {str(e)}")
            raise
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_symbol = symbol.replace('/', '_')
            
            response = requests.get(
                f"{self.BASE_URL}/spot/quotation/v3/books",
                params={"symbol": api_symbol, "limit": min(limit, 50)},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 1000:
                raise Exception(f"BitMart API error: {result.get('message')}")
            
            data = result.get('data', {})
            
            asks = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in data.get('asks', [])]
            bids = [[self._safe_float(item[0]), self._safe_float(item[1])] 
                    for item in data.get('bids', [])]
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
                timestamp=data.get('ts')
            )
            
        except requests.RequestException as e:
            logger.error(f"BitMart orderbook API error: {str(e)}")
            raise Exception(f"Failed to fetch BitMart orderbook: {str(e)}")
        except Exception as e:
            logger.error(f"BitMart orderbook processing error: {str(e)}")
            raise
