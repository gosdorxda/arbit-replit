import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class AzbitAdapter(BaseAdapter):
    BASE_URL = "https://data.azbit.com/api"
    
    @property
    def exchange_name(self) -> str:
        return "AZBIT"
    
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
                pair_code = item.get('currencyPairCode', '')
                if not pair_code.endswith('_USDT'):
                    continue
                
                base = pair_code.replace('_USDT', '')
                
                price = self._safe_float(item.get('price'))
                volume_24h = self._safe_float(item.get('volume24h'))
                high_24h = self._safe_float(item.get('high24h'))
                low_24h = self._safe_float(item.get('low24h'))
                change_24h = self._safe_float(item.get('priceChangePercentage24h', 0))
                turnover_24h = price * volume_24h if price and volume_24h else 0
                
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
            
            logger.info(f"Azbit: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Azbit API error: {str(e)}")
            raise Exception(f"Failed to fetch Azbit data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '')
            api_symbol = f"{base}_USDT"
            
            response = requests.get(
                f"{self.BASE_URL}/orderbook/{api_symbol}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            asks = []
            for ask in data.get('asks', [])[:limit]:
                price = self._safe_float(ask.get('price'))
                amount = self._safe_float(ask.get('quantity'))
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in data.get('bids', [])[:limit]:
                price = self._safe_float(bid.get('price'))
                amount = self._safe_float(bid.get('quantity'))
                if price and amount:
                    bids.append({'price': price, 'amount': amount})
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"Azbit orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch Azbit orderbook: {str(e)}")
