import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class DigiFinexAdapter(BaseAdapter):
    BASE_URL = "https://openapi.digifinex.com/v3"
    
    @property
    def exchange_name(self) -> str:
        return "DIGIFINEX"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/ticker",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') != 0:
                raise Exception(f"API error code: {data.get('code')}")
            
            tickers = []
            ticker_list = data.get('ticker', [])
            
            for item in ticker_list:
                symbol = item.get('symbol', '')
                if not symbol.endswith('_usdt'):
                    continue
                
                base = symbol.replace('_usdt', '').upper()
                
                price = self._safe_float(item.get('last'))
                volume_24h = self._safe_float(item.get('vol'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                change_24h = self._safe_float(item.get('change', 0))
                turnover_24h = self._safe_float(item.get('base_vol', 0))
                
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
            
            logger.info(f"DigiFinex: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"DigiFinex API error: {str(e)}")
            raise Exception(f"Failed to fetch DigiFinex data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '')
            api_symbol = f"{base.lower()}_usdt"
            
            response = requests.get(
                f"{self.BASE_URL}/order_book",
                params={
                    "symbol": api_symbol,
                    "limit": limit
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') != 0:
                raise Exception(f"API error code: {data.get('code')}")
            
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
            logger.error(f"DigiFinex orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch DigiFinex orderbook: {str(e)}")
