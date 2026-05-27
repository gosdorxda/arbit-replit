import json
import gzip
import logging
import threading
from typing import List
import websocket
from .base import BaseAdapter, NormalizedTicker, NormalizedOrderbook

logger = logging.getLogger(__name__)

WSS_URL = "wss://api.uzx.com/notification/ws"


class UZXAdapter(BaseAdapter):

    @property
    def exchange_name(self) -> str:
        return "UZX"

    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        results = []
        done = threading.Event()
        error_holder = []

        def on_message(ws, msg):
            try:
                try:
                    data = gzip.decompress(msg)
                except Exception:
                    data = msg if isinstance(msg, bytes) else msg.encode()
                j = json.loads(data)
                if j.get("code") == 200 and isinstance(j.get("data"), list) and len(j["data"]) > 1:
                    results.extend(j["data"])
                    done.set()
                    ws.close()
            except Exception as e:
                logger.warning(f"UZX ws parse error: {e}")

        def on_open(ws):
            sub = json.dumps({
                "event": "sub",
                "params": {
                    "biz": "market",
                    "type": "spot.overview",
                    "symbol": "",
                    "interval": ""
                },
                "zip": False
            })
            ws.send(sub)

        def on_error(ws, err):
            logger.error(f"UZX ws error: {err}")
            error_holder.append(str(err))
            done.set()

        ws = websocket.WebSocketApp(
            WSS_URL,
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
        )
        t = threading.Thread(target=ws.run_forever)
        t.daemon = True
        t.start()
        done.wait(timeout=20)

        if error_holder and not results:
            raise Exception(f"UZX WebSocket error: {error_holder[0]}")
        if not results:
            raise Exception("UZX: No ticker data received within timeout")

        tickers = []
        for item in results:
            symbol_raw = item.get("symbol", "")
            market = item.get("market", {})

            if not symbol_raw.endswith("-USDT"):
                continue

            base = symbol_raw.replace("-USDT", "")
            price = self._safe_float(market.get("close"))
            if not price or price <= 0:
                continue

            open_price = self._safe_float(market.get("open"))
            high_24h = self._safe_float(market.get("high"))
            low_24h = self._safe_float(market.get("low"))
            volume_24h = self._safe_float(market.get("vol"))
            turnover_24h = self._safe_float(market.get("turn_over"))
            change_percent = self._safe_float(market.get("change_percent"))

            if open_price and not change_percent:
                change_percent = ((price - open_price) / open_price * 100) if open_price else 0.0

            tickers.append(NormalizedTicker(
                exchange=self.exchange_name,
                symbol=f"{base}/USDT",
                base_currency=base,
                quote_currency="USDT",
                price=price,
                volume_24h=volume_24h,
                high_24h=high_24h,
                low_24h=low_24h,
                change_24h=change_percent,
                turnover_24h=turnover_24h,
            ))

        logger.info(f"UZX: Fetched {len(tickers)} USDT pairs")
        return tickers

    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        """UZX has no orderbook depth channel — use spot.ticker for best bid/ask."""
        uzx_symbol = symbol.replace("/", "-")
        result_holder = []
        done = threading.Event()

        def on_message(ws, msg):
            try:
                try:
                    data = gzip.decompress(msg)
                except Exception:
                    data = msg if isinstance(msg, bytes) else msg.encode()
                j = json.loads(data)
                msg_type = j.get("type", "")
                if "ticker" in msg_type and j.get("data"):
                    result_holder.append(j["data"])
                    done.set()
                    ws.close()
            except Exception as e:
                logger.warning(f"UZX orderbook parse: {e}")

        def on_open(ws):
            sub = json.dumps({
                "event": "sub",
                "params": {
                    "biz": "market",
                    "type": "spot.ticker",
                    "symbol": uzx_symbol,
                    "interval": ""
                },
                "zip": False
            })
            ws.send(sub)

        def on_error(ws, err):
            logger.error(f"UZX orderbook ws error: {err}")
            done.set()

        ws = websocket.WebSocketApp(
            WSS_URL,
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
        )
        t = threading.Thread(target=ws.run_forever)
        t.daemon = True
        t.start()
        done.wait(timeout=10)

        if not result_holder:
            return NormalizedOrderbook(exchange=self.exchange_name, symbol=symbol, asks=[], bids=[])

        ticker = result_holder[0]
        ask_price = self._safe_float(ticker.get("ask_price"))
        ask_vol   = self._safe_float(ticker.get("ask_vol"))
        bid_price = self._safe_float(ticker.get("bid_price"))
        bid_vol   = self._safe_float(ticker.get("bid_vol"))

        asks = [{"price": ask_price, "amount": ask_vol}] if ask_price and ask_vol else []
        bids = [{"price": bid_price, "amount": bid_vol}] if bid_price and bid_vol else []

        return NormalizedOrderbook(
            exchange=self.exchange_name,
            symbol=symbol,
            asks=asks,
            bids=bids,
        )
