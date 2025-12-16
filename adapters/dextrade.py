import requests
import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)


class DexTradeAdapter(BaseAdapter):
    BASE_URL = "https://api.dex-trade.com/v1/public"
    
    @property
    def exchange_name(self) -> str:
        return "DEXTRADE"
    
    def _fetch_single_ticker(self, session, pair_info):
        pair_name = pair_info.get('pair', '')
        base = pair_info.get('base', '')
        
        try:
            ticker_response = session.get(
                f"{self.BASE_URL}/ticker",
                params={"pair": pair_name},
                timeout=5
            )
            
            if ticker_response.status_code != 200:
                return None
            
            ticker_data = ticker_response.json()
            
            if not ticker_data or 'error' in ticker_data:
                return None
            
            data = ticker_data.get('data', ticker_data)
            
            last_price = self._safe_float(data.get('last'))
            volume_24h = self._safe_float(data.get('volume_24H', data.get('volume')))
            high_24h = self._safe_float(data.get('high'))
            low_24h = self._safe_float(data.get('low'))
            change_24h = self._safe_float(data.get('percent_сhange', data.get('percent_change', 0)))
            
            turnover_24h = volume_24h * last_price if volume_24h and last_price else 0
            
            return NormalizedTicker(
                exchange=self.exchange_name,
                symbol=f"{base}/USDT",
                base_currency=base,
                quote_currency='USDT',
                price=last_price,
                volume_24h=volume_24h,
                high_24h=high_24h,
                low_24h=low_24h,
                change_24h=change_24h,
                turnover_24h=turnover_24h
            )
        except Exception as e:
            logger.debug(f"Dex-Trade: Failed to fetch ticker for {pair_name}: {e}")
            return None
    
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            session = requests.Session()
            
            symbols_response = session.get(
                f"{self.BASE_URL}/symbols",
                timeout=30
            )
            symbols_response.raise_for_status()
            symbols_data = symbols_response.json()
            
            if not symbols_data.get('status'):
                raise Exception("Failed to fetch symbols from Dex-Trade")
            
            usdt_pairs = [
                s for s in symbols_data.get('data', [])
                if s.get('quote') == 'USDT'
            ]
            
            logger.info(f"Dex-Trade: Found {len(usdt_pairs)} USDT pairs, fetching tickers concurrently...")
            
            tickers = []
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(self._fetch_single_ticker, session, pair): pair 
                          for pair in usdt_pairs}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        tickers.append(result)
            
            logger.info(f"Dex-Trade: Fetched {len(tickers)} USDT pairs")
            return tickers
            
        except requests.RequestException as e:
            logger.error(f"Dex-Trade API error: {str(e)}")
            raise Exception(f"Failed to fetch Dex-Trade data: {str(e)}")
        except Exception as e:
            logger.error(f"Dex-Trade processing error: {str(e)}")
            raise
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            api_pair = symbol.replace('/', '')
            
            response = requests.get(
                f"{self.BASE_URL}/book",
                params={"pair": api_pair},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if not result.get('status'):
                raise Exception(f"Dex-Trade API error")
            
            data = result.get('data', {})
            
            sell_orders = data.get('sell', [])[:limit]
            buy_orders = data.get('buy', [])[:limit]
            
            asks = [[self._safe_float(item.get('rate')), self._safe_float(item.get('volume'))] 
                    for item in sell_orders]
            bids = [[self._safe_float(item.get('rate')), self._safe_float(item.get('volume'))] 
                    for item in buy_orders]
            
            return NormalizedOrderbook(
                exchange=self.exchange_name,
                symbol=symbol,
                asks=asks,
                bids=bids,
                timestamp=data.get('sequenceId')
            )
            
        except requests.RequestException as e:
            logger.error(f"Dex-Trade orderbook API error: {str(e)}")
            raise Exception(f"Failed to fetch Dex-Trade orderbook: {str(e)}")
        except Exception as e:
            logger.error(f"Dex-Trade orderbook processing error: {str(e)}")
            raise
