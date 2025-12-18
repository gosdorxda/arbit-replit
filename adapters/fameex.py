import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class FameEXAdapter(BaseAdapter):
    BASE_URL = "https://openapi.fameex.com"
    
    @property
    def exchange_name(self) -> str:
        return "FAMEEX"
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/v2/public/ticker",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            tickers = []
            ticker_list = data if isinstance(data, list) else data.get('data', [])
            
            for item in ticker_list:
                trading_pairs = item.get('trading_pairs', '') or item.get('symbol', '')
                if not trading_pairs:
                    continue
                
                if '_' in trading_pairs:
                    parts = trading_pairs.split('_')
                    base = parts[0].upper()
                    quote = parts[1].upper() if len(parts) > 1 else ''
                elif 'USDT' in trading_pairs.upper():
                    upper_pair = trading_pairs.upper()
                    base = upper_pair.replace('USDT', '')
                    quote = 'USDT'
                else:
                    continue
                
                if quote != 'USDT':
                    continue
                
                price = self._safe_float(item.get('last_price') or item.get('last'))
                volume_24h = self._safe_float(item.get('base_volume') or item.get('vol'))
                turnover_24h = self._safe_float(item.get('quote_volume') or item.get('amount'))
                high_24h = self._safe_float(item.get('high_24h') or item.get('high'))
                low_24h = self._safe_float(item.get('low_24h') or item.get('low'))
                
                change_str = item.get('price_change_percent_24h') or item.get('rose') or '0'
                if isinstance(change_str, str):
                    change_str = change_str.replace('%', '').replace('+', '')
                change_24h = self._safe_float(change_str)
                
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
            
            logger.info(f"FameEX: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"FameEX API error: {str(e)}")
            raise Exception(f"Failed to fetch FameEX data: {str(e)}")
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.replace('/USDT', '')
            api_symbol = f"{base}_USDT"
            
            response = requests.get(
                f"{self.BASE_URL}/v2/public/orderbook/{api_symbol}",
                params={"depth": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            order_data = data.get('data', data) if isinstance(data, dict) else data
            
            asks = []
            for ask in order_data.get('asks', []):
                if isinstance(ask, list) and len(ask) >= 2:
                    price = self._safe_float(ask[0])
                    amount = self._safe_float(ask[1])
                elif isinstance(ask, dict):
                    price = self._safe_float(ask.get('price'))
                    amount = self._safe_float(ask.get('quantity') or ask.get('amount'))
                else:
                    continue
                if price and amount:
                    asks.append({'price': price, 'amount': amount})
            
            bids = []
            for bid in order_data.get('bids', []):
                if isinstance(bid, list) and len(bid) >= 2:
                    price = self._safe_float(bid[0])
                    amount = self._safe_float(bid[1])
                elif isinstance(bid, dict):
                    price = self._safe_float(bid.get('price'))
                    amount = self._safe_float(bid.get('quantity') or bid.get('amount'))
                else:
                    continue
                if price and amount:
                    bids.append({'price': price, 'amount': amount})
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids
            )
            
        except requests.RequestException as e:
            logger.error(f"FameEX orderbook error: {str(e)}")
            raise Exception(f"Failed to fetch FameEX orderbook: {str(e)}")
