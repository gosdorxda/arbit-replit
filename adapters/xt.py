import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class XTAdapter(BaseAdapter):
    BASE_URL = "https://sapi.xt.com"
    
    @property
    def exchange_name(self) -> str:
        return "XT"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/v4/public/ticker",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            result = data.get('result', [])
            
            for item in result:
                symbol = item.get('s', '')
                if not symbol.endswith('_usdt'):
                    continue
                
                base = symbol.replace('_usdt', '').upper()
                
                price = self._safe_float(item.get('c'))
                volume_24h = self._safe_float(item.get('q'))
                high_24h = self._safe_float(item.get('h'))
                low_24h = self._safe_float(item.get('l'))
                change_24h = self._safe_float(item.get('cr'))
                turnover_24h = self._safe_float(item.get('v'))
                
                if change_24h is not None:
                    change_24h = change_24h * 100
                
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
            
            logger.info(f"XT.com: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"XT.com API error: {str(e)}")
            raise Exception(f"Failed to fetch XT.com data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '').replace('/', '').lower()
            api_symbol = f"{base}_usdt"
            
            response = requests.get(
                f"{self.BASE_URL}/v4/public/depth",
                params={
                    "symbol": api_symbol,
                    "limit": limit
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            result = data.get('result', {})
            
            asks = []
            for ask in result.get('asks', []):
                if len(ask) >= 2:
                    price = self._safe_float(ask[0])
                    amount = self._safe_float(ask[1])
                    if price and amount:
                        asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in result.get('bids', []):
                if len(bid) >= 2:
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
            logger.error(f"XT.com orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch XT.com orderbook: {str(e)}")
