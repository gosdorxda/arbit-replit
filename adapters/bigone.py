import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class BigOneAdapter(BaseAdapter):
    BASE_URL = "https://big.one/api/v3"
    
    @property
    def exchange_name(self) -> str:
        return "BIGONE"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/asset_pairs/tickers",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            data = result.get('data', []) if isinstance(result, dict) else result
            
            tickers = []
            for item in data:
                pair_name = item.get('asset_pair_name', '')
                if not pair_name.endswith('-USDT'):
                    continue
                
                base = pair_name.replace('-USDT', '')
                
                price = self._safe_float(item.get('close'))
                volume_24h = self._safe_float(item.get('volume'))
                high_24h = self._safe_float(item.get('high'))
                low_24h = self._safe_float(item.get('low'))
                
                open_price = self._safe_float(item.get('open'))
                daily_change = self._safe_float(item.get('daily_change'))
                
                if price and open_price and open_price > 0:
                    change_24h = ((price - open_price) / open_price) * 100
                elif daily_change and open_price and open_price > 0:
                    change_24h = (daily_change / open_price) * 100
                else:
                    change_24h = 0
                
                turnover_24h = None
                if price and volume_24h:
                    turnover_24h = price * volume_24h
                
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
            
            logger.info(f"BigOne: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"BigOne API error: {str(e)}")
            raise Exception(f"Failed to fetch BigOne data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            api_symbol = f"{base}-USDT"
            
            response = requests.get(
                f"{self.BASE_URL}/asset_pairs/{api_symbol}/depth",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            data = result.get('data', {}) if isinstance(result, dict) else result
            
            asks = []
            for ask in data.get('asks', [])[:limit]:
                price = self._safe_float(ask.get('price'))
                amount = self._safe_float(ask.get('quantity') or ask.get('amount'))
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in data.get('bids', [])[:limit]:
                price = self._safe_float(bid.get('price'))
                amount = self._safe_float(bid.get('quantity') or bid.get('amount'))
                if price and amount:
                    bids.append({'price': price, 'amount': amount})
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"BigOne orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch BigOne orderbook: {str(e)}")
