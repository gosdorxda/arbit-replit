import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class P2PB2BAdapter(BaseAdapter):
    BASE_URL = "https://api.p2pb2b.com/api/v2/public"
    
    @property
    def exchange_name(self) -> str:
        return "P2PB2B"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/tickers",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                raise Exception(f"API error: {data.get('message', 'Unknown error')}")
            
            tickers = []
            result = data.get('result', {})
            
            for market_name, market_data in result.items():
                if not market_name.endswith('_USDT'):
                    continue
                
                base = market_name.replace('_USDT', '')
                ticker_data = market_data.get('ticker', {})
                
                price = self._safe_float(ticker_data.get('last'))
                volume_24h = self._safe_float(ticker_data.get('vol'))
                high_24h = self._safe_float(ticker_data.get('high'))
                low_24h = self._safe_float(ticker_data.get('low'))
                change_24h = self._safe_float(ticker_data.get('change', 0))
                turnover_24h = self._safe_float(ticker_data.get('deal', 0))
                
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
            
            logger.info(f"P2PB2B: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"P2PB2B API error: {str(e)}")
            raise Exception(f"Failed to fetch P2PB2B data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '')
            api_symbol = f"{base}_USDT"
            
            asks = []
            bids = []
            
            for side in ['sell', 'buy']:
                response = requests.get(
                    f"{self.BASE_URL}/book",
                    params={
                        "market": api_symbol,
                        "side": side,
                        "limit": limit
                    },
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                if not data.get('success'):
                    raise Exception(f"API error: {data.get('message', 'Unknown error')}")
                
                orders = data.get('result', {}).get('orders', [])
                
                for order in orders:
                    price = self._safe_float(order.get('price'))
                    amount = self._safe_float(order.get('left'))
                    if price and amount:
                        order_entry = {'price': price, 'amount': amount}
                        if side == 'sell':
                            asks.append(order_entry)
                        else:
                            bids.append(order_entry)
            
            asks.sort(key=lambda x: x['price'])
            bids.sort(key=lambda x: x['price'], reverse=True)
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"P2PB2B orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch P2PB2B orderbook: {str(e)}")
