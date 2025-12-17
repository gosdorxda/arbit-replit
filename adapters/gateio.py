import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class GateIOAdapter(BaseAdapter):
    BASE_URL = "https://api.gateio.ws/api/v4"
    
    @property
    def exchange_name(self) -> str:
        return "GATEIO"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/spot/tickers",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                currency_pair = item.get('currency_pair', '')
                if not currency_pair.endswith('_USDT'):
                    continue
                
                base = currency_pair.replace('_USDT', '')
                
                price = self._safe_float(item.get('last'))
                volume_24h = self._safe_float(item.get('base_volume'))
                high_24h = self._safe_float(item.get('high_24h'))
                low_24h = self._safe_float(item.get('low_24h'))
                change_24h = self._safe_float(item.get('change_percentage', 0))
                turnover_24h = self._safe_float(item.get('quote_volume', 0))
                
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
            
            logger.info(f"Gate.io: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Gate.io API error: {str(e)}")
            raise Exception(f"Failed to fetch Gate.io data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '')
            api_symbol = f"{base}_USDT"
            
            response = requests.get(
                f"{self.BASE_URL}/spot/order_book",
                params={
                    "currency_pair": api_symbol,
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
            logger.error(f"Gate.io orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Gate.io orderbook: {str(e)}")
