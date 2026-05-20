import requests
import logging
from typing import List
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)

# Module-level cache: base_symbol_upper -> alphaId (e.g. "NEX" -> "ALPHA_971")
_ALPHA_ID_CACHE: dict = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


class BinanceAlphaAdapter(BaseAdapter):
    TOKEN_LIST_URL = (
        "https://www.binance.com/bapi/defi/v1/public/"
        "wallet-direct/buw/wallet/cex/alpha/all/token/list"
    )
    TICKER_URL = (
        "https://www.binance.com/bapi/defi/v1/public/alpha-trade/ticker"
    )
    DEPTH_URL = (
        "https://www.binance.com/bapi/defi/v1/public/alpha-trade/depth"
    )

    @property
    def exchange_name(self) -> str:
        return "BINANCEALPHA"

    def _fetch_token_list(self) -> list:
        resp = requests.get(self.TOKEN_LIST_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            raise Exception(f"Binance Alpha token list error: {data.get('message')}")
        return data.get("data", [])

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        try:
            tokens = self._fetch_token_list()
            # Deduplicate by base symbol — keep highest turnover per symbol
            best: dict = {}
            for token in tokens:
                if token.get("offline", False) or token.get("fullyDelisted", False):
                    continue
                raw_symbol = token.get("symbol", "")
                alpha_id = token.get("alphaId", "")
                if not raw_symbol or not alpha_id:
                    continue
                base = raw_symbol.upper()
                turnover = self._safe_float(token.get("volume24h")) or 0.0
                prev = best.get(base)
                if prev is None or turnover > (self._safe_float(prev.get("volume24h")) or 0.0):
                    best[base] = token

            tickers = []
            for base, token in best.items():
                alpha_id = token.get("alphaId", "")
                _ALPHA_ID_CACHE[base] = alpha_id

                price = self._safe_float(token.get("price"))
                turnover = self._safe_float(token.get("volume24h"))
                change = self._safe_float(token.get("percentChange24h"))
                high = self._safe_float(token.get("priceHigh24h"))
                low = self._safe_float(token.get("priceLow24h"))

                tickers.append(NormalizedTicker(
                    exchange=self.exchange_name,
                    symbol=f"{base}/USDT",
                    base_currency=base,
                    quote_currency="USDT",
                    price=price,
                    volume_24h=None,
                    high_24h=high,
                    low_24h=low,
                    change_24h=change,
                    turnover_24h=turnover,
                ))

            logger.info(f"BinanceAlpha: fetched {len(tickers)} active tokens")
            return tickers

        except requests.RequestException as e:
            logger.error(f"BinanceAlpha API error: {e}")
            raise Exception(f"Failed to fetch BinanceAlpha data: {e}")
        except Exception as e:
            logger.error(f"BinanceAlpha processing error: {e}")
            raise

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        try:
            base = symbol.split("/")[0].upper()

            # Ensure cache is populated
            if base not in _ALPHA_ID_CACHE:
                for token in self._fetch_token_list():
                    sym = token.get("symbol", "").upper()
                    aid = token.get("alphaId", "")
                    if sym and aid:
                        _ALPHA_ID_CACHE[sym] = aid

            alpha_id = _ALPHA_ID_CACHE.get(base)
            if not alpha_id:
                return NormalizedOrderbook(
                    exchange=self.exchange_name, symbol=symbol, asks=[], bids=[]
                )

            trading_symbol = f"{alpha_id}USDT"
            resp = requests.get(
                self.DEPTH_URL,
                params={"symbol": trading_symbol, "limit": limit},
                headers=HEADERS,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()

            ob = data.get("data", data)
            asks = [
                [self._safe_float(i[0]), self._safe_float(i[1])]
                for i in ob.get("asks", [])
            ]
            bids = [
                [self._safe_float(i[0]), self._safe_float(i[1])]
                for i in ob.get("bids", [])
            ]
            return NormalizedOrderbook(
                exchange=self.exchange_name, symbol=symbol, asks=asks, bids=bids
            )

        except Exception as e:
            logger.error(f"BinanceAlpha orderbook error: {e}")
            return NormalizedOrderbook(
                exchange=self.exchange_name, symbol=symbol, asks=[], bids=[]
            )
