import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker

logger = logging.getLogger(__name__)


class LBankAdapter(BaseAdapter):
    BASE_URL = "https://api.lbkex.com"
    
    @property
    def exchange_name(self) -> str:
        return "LBANK"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/v1/ticker.do",
                params={"symbol": "all"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                symbol = item.get('symbol', '')
                
                if not symbol.endswith('_usdt'):
                    continue
                
                base_currency = symbol.replace('_usdt', '').upper()
                ticker_data = item.get('ticker', {})
                
                normalized = NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=symbol.upper().replace('_', '/'),
                    base_currency=base_currency,
                    quote_currency='USDT',
                    price=self._safe_float(ticker_data.get('latest')),
                    volume_24h=self._safe_float(ticker_data.get('vol')),
                    high_24h=self._safe_float(ticker_data.get('high')),
                    low_24h=self._safe_float(ticker_data.get('low')),
                    change_24h=self._safe_float(ticker_data.get('change')),
                    turnover_24h=self._safe_float(ticker_data.get('turnover'))
                )
                tickers.append(normalized)
            
            logger.info(f"LBANK: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"LBANK API error: {str(e)}")
            raise Exception(f"Failed to fetch LBANK data: {str(e)}")
        except Exception as e:
            logger.error(f"LBANK processing error: {str(e)}")
            raise
