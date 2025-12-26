import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class LatokenAdapter(BaseAdapter):
    BASE_URL = "https://api.latoken.com/v2"
    
    def __init__(self):
        super().__init__()
        self._currencies = {}
        self._pairs = {}
    
    @property
    def exchange_name(self) -> str:
        return "LATOKEN"
    
    def _load_currencies(self):
        if not self._currencies:
            response = requests.get(f"{self.BASE_URL}/currency", timeout=30)
            response.raise_for_status()
            for curr in response.json():
                self._currencies[curr.get('id')] = curr.get('tag', '')
    
    def _load_pairs(self):
        if not self._pairs:
            response = requests.get(f"{self.BASE_URL}/pair", timeout=30)
            response.raise_for_status()
            for pair in response.json():
                self._pairs[pair.get('id')] = {
                    'baseCurrency': pair.get('baseCurrency'),
                    'quoteCurrency': pair.get('quoteCurrency'),
                    'symbol': pair.get('symbol', '')
                }
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            self._load_currencies()
            self._load_pairs()
            
            response = requests.get(
                f"{self.BASE_URL}/ticker",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            usdt_id = None
            for curr_id, symbol in self._currencies.items():
                if symbol == 'USDT':
                    usdt_id = curr_id
                    break
            
            tickers = []
            
            for item in data:
                quote_currency = item.get('quoteCurrency', '')
                if quote_currency != usdt_id:
                    continue
                
                base_currency_id = item.get('baseCurrency', '')
                base = self._currencies.get(base_currency_id, '')
                
                if not base:
                    continue
                
                price = self._safe_float(item.get('lastPrice'))
                volume_24h = self._safe_float(item.get('volume24h'))
                high_24h = self._safe_float(item.get('high24h', 0))
                low_24h = self._safe_float(item.get('low24h', 0))
                change_24h = self._safe_float(item.get('change24h', 0)) * 100
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
            
            logger.info(f"LATOKEN: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"LATOKEN API error: {str(e)}")
            raise Exception(f"Failed to fetch LATOKEN data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            self._load_currencies()
            
            base = symbol.replace('/USDT', '').replace('/', '')
            
            base_id = None
            usdt_id = None
            for curr_id, curr_symbol in self._currencies.items():
                if curr_symbol == base:
                    base_id = curr_id
                if curr_symbol == 'USDT':
                    usdt_id = curr_id
            
            if not base_id or not usdt_id:
                raise Exception(f"Currency not found: {base}")
            
            response = requests.get(
                f"{self.BASE_URL}/book/{base_id}/{usdt_id}",
                params={"limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            asks = []
            for ask in data.get('ask', [])[:limit]:
                price = self._safe_float(ask.get('price'))
                amount = self._safe_float(ask.get('quantity'))
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in data.get('bid', [])[:limit]:
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
            logger.error(f"LATOKEN orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch LATOKEN orderbook: {str(e)}")
