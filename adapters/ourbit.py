import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class OurbitAdapter(BaseAdapter):
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    @property
    def exchange_name(self) -> str:
        return "OURBIT"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            tickers = []
            page = 1
            max_pages = 10
            
            while page <= max_pages:
                response = requests.get(
                    f"{self.BASE_URL}/exchanges/ourbit/tickers",
                    params={"page": page},
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                
                page_tickers = result.get('tickers', [])
                if not page_tickers:
                    break
                
                for item in page_tickers:
                    target = item.get('target', '')
                    if target != 'USDT':
                        continue
                    
                    base = item.get('base', '')
                    if not base:
                        continue
                    
                    price = self._safe_float(item.get('last'))
                    volume_24h = self._safe_float(item.get('volume'))
                    
                    converted_volume = item.get('converted_volume', {})
                    turnover_24h = self._safe_float(converted_volume.get('usd'))
                    
                    normalized = NormalizedTicker(
                        exchange=self.exchange_name,
                        symbol=f"{base}/USDT",
                        base_currency=base,
                        quote_currency='USDT',
                        price=price,
                        volume_24h=volume_24h,
                        high_24h=None,
                        low_24h=None,
                        change_24h=0,
                        turnover_24h=turnover_24h
                    )
                    tickers.append(normalized)
                
                page += 1
            
            logger.info(f"Ourbit: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Ourbit API error: {str(e)}")
            raise Exception(f"Failed to fetch Ourbit data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        return NormalizedOrderbook(
            exchange=self.exchange_name,
            symbol=symbol,
            asks=[],
            bids=[],
            error="Ourbit orderbook not available (no public API)"
        )
