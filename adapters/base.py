from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class NormalizedOrderbook:
    exchange: str
    symbol: str
    asks: List[List[float]] = field(default_factory=list)
    bids: List[List[float]] = field(default_factory=list)
    timestamp: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'symbol': self.symbol,
            'asks': self.asks,
            'bids': self.bids,
            'timestamp': self.timestamp
        }


@dataclass
class NormalizedTicker:
    exchange: str
    symbol: str
    base_currency: str
    quote_currency: str
    price: float
    volume_24h: float
    high_24h: float
    low_24h: float
    change_24h: float
    turnover_24h: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'symbol': self.symbol,
            'base_currency': self.base_currency,
            'quote_currency': self.quote_currency,
            'price': self.price,
            'volume_24h': self.volume_24h,
            'high_24h': self.high_24h,
            'low_24h': self.low_24h,
            'change_24h': self.change_24h,
            'turnover_24h': self.turnover_24h
        }


class BaseAdapter(ABC):
    
    @property
    @abstractmethod
    def exchange_name(self) -> str:
        pass
    
    @abstractmethod
    def fetch_usdt_tickers(self) -> List[NormalizedTicker]:
        pass
    
    @abstractmethod
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> NormalizedOrderbook:
        pass
    
    def _safe_float(self, value, default=0.0) -> float:
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
