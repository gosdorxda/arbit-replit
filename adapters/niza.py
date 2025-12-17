import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class NizaAdapter(BaseAdapter):
    BASE_URL = "https://app.niza.io/trade/v1"
    
    @property
    def exchange_name(self) -> str:
        return "NIZA"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/tickers",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            for item in data:
                target_currency = item.get('target_currency', '')
                if target_currency != 'USDT':
                    continue
                
                base = item.get('base_currency', '')
                
                price = self._safe_float(item.get('last_price'))
                volume_24h = self._safe_float(item.get('base_volume'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                turnover_24h = self._safe_float(item.get('target_volume', 0))
                
                change_24h = 0.0
                
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
            
            logger.info(f"Niza: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Niza API error: {str(e)}")
            raise Exception(f"Failed to fetch Niza data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            ticker_id = symbol.replace('/', '%2F')
            
            response = requests.get(
                f"{self.BASE_URL}/orderbook",
                params={
                    "ticker_id": symbol,
                    "depth": limit
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            orderbook_data = data[0] if isinstance(data, list) and len(data) > 0 else data
            
            asks = []
            for ask in orderbook_data.get('asks', []):
                price = self._safe_float(ask[0])
                amount = self._safe_float(ask[1])
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in orderbook_data.get('bids', []):
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
            logger.error(f"Niza orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Niza orderbook: {str(e)}")
